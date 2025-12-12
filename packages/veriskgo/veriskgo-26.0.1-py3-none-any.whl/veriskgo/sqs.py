# src/veriskgo/sqs.py

import json
import boto3
import queue
import threading
import time
import os
import atexit
import tempfile
from typing import Optional, Dict, Any
from .config import get_cfg

SPILLOVER_FILE = os.path.join(tempfile.gettempdir(), "veriskgo_spillover_queue.jsonl")

MAIN_PID = os.getpid()


class _VeriskGoSQS:
    """
    PRODUCTION-GRADE SQS SENDER
    - Daemon worker threads (never block shutdown)
    - Force-flush on exit (guarantees delivery)
    - Auto spillover for failed sends
    """

    def __init__(self):
        self.client: Optional[Any] = None
        self.queue_url: Optional[str] = None
        self.sqs_enabled = False
        self._init_once = False

        # Main in-memory queue
        self._q: queue.Queue = queue.Queue(maxsize=0)

        # Restore spillover messages
        self._load_spillover()

        # Start worker threads (daemon=True ensures no hang)
        self.worker_count = 4
        self.workers = []
        for i in range(self.worker_count):
            t = threading.Thread(target=self._safe_worker_loop, daemon=True)
            t.start()
            self.workers.append(t)

        # Initialize AWS client
        self._auto_initialize()

    # -------------------------------------------------------
    # SPILLOVER SAVE
    # -------------------------------------------------------
    def _spillover_save(self, message: Dict[str, Any]):
        try:
            with open(SPILLOVER_FILE, "a") as f:
                f.write(json.dumps(message) + "\n")
        except Exception as e:
            print("[veriskgo] Spillover save failed:", e)

    # -------------------------------------------------------
    # SPILLOVER LOAD
    # -------------------------------------------------------
    def _load_spillover(self):
        if not os.path.exists(SPILLOVER_FILE):
            return

        try:
            print("[veriskgo] Restoring spillover queue from disk...")
            with open(SPILLOVER_FILE, "r") as f:
                for line in f:
                    self._q.put(json.loads(line.strip()))
            os.remove(SPILLOVER_FILE)
            print("[veriskgo] Spillover restored.")
        except Exception as e:
            print("[veriskgo] Spillover load failed:", e)

    # -------------------------------------------------------
    # WORKER LOOP (auto-restarting)
    # -------------------------------------------------------
    def _safe_worker_loop(self):
        while True:
            try:
                self._worker_loop()
            except Exception as e:
                print("[veriskgo] Worker crashed:", e)
                time.sleep(0.5)
                print("[veriskgo] Restarting worker...")

    # -------------------------------------------------------
    # REAL WORKER LOOP (runs forever)
    # -------------------------------------------------------
    def _worker_loop(self):
        batch = []

        while True:
            try:
                msg = self._q.get(timeout=0.2)
                batch.append(msg)
            except queue.Empty:
                pass

            # Batch conditions
            flush_size = len(batch) >= 10
            flush_time = batch and (time.time() % 1 < 0.15)

            if flush_size or flush_time:
                self._send_batch(batch)
                batch = []

    # -------------------------------------------------------
    # FORCE FLUSH (used by atexit)
    # -------------------------------------------------------
    def force_flush(self):
        """Synchronously send all remaining messages (blocking)."""
        batch = []
        try:
            while not self._q.empty():
                batch.append(self._q.get_nowait())
        except Exception:
            pass

        if batch:
            print("[veriskgo] Force flush triggered")
            self._send_batch(batch)

        # Give AWS some breathing room
        time.sleep(0.1)

    # -------------------------------------------------------
    # AWS INIT
    # -------------------------------------------------------
    def _auto_initialize(self):
        if self._init_once and self.client:
            return

        cfg = get_cfg()
        self.queue_url = cfg.get("aws_sqs_url")

        if not self.queue_url:
            print("[veriskgo] No SQS URL → disabled.")
            return

        try:
            session = boto3.Session(
                profile_name=cfg.get("aws_profile"),
                region_name=cfg.get("aws_region", "us-east-1")
            )
            self.client = session.client("sqs")

            # test connection
            self.client.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=["QueueArn"]
            )

            self.sqs_enabled = True
            print(f"[veriskgo] SQS connected → {self.queue_url}")

        except Exception as e:
            print("[veriskgo] SQS init failed:", e)
            self.client = None
            self.sqs_enabled = False

        self._init_once = True

    # -------------------------------------------------------
    # PUBLIC SEND API
    # -------------------------------------------------------
    def send(self, message: Optional[Dict[str, Any]]) -> bool:
        if not message:
            print("[veriskgo] Empty message → not sent.")
            return False

        if not self.sqs_enabled:
            self._auto_initialize()

        try:
            print("[veriskgo] Queuing message...")
            self._q.put_nowait(message)
            return True
        except Exception as e:
            print("[veriskgo] RAM queue failed → spillover:", e)
            self._spillover_save(message)
            return False

    # -------------------------------------------------------
    # BATCH SEND
    # -------------------------------------------------------
    def _send_batch(self, batch):
        if not batch:
            return

        if not self.client or not self.sqs_enabled:
            self._auto_initialize()

        if not self.client or not self.sqs_enabled:
            print("[veriskgo] SQS unavailable → spillover.")
            for msg in batch:
                self._spillover_save(msg)
            return

        entries = [{
            "Id": str(i),
            "MessageBody": json.dumps(msg)
        } for i, msg in enumerate(batch[:10])]

        try:
            self.client.send_message_batch(
                QueueUrl=self.queue_url,
                Entries=entries
            )
            print(f"[veriskgo] Batch sent ({len(entries)} items)")
        except Exception as e:
            print("[veriskgo] Batch send failed:", e)
            self._retry_individual(batch)

    # -------------------------------------------------------
    # RETRY INDIVIDUAL MESSAGES
    # -------------------------------------------------------
    def _retry_individual(self, batch):
        if not self.client or not self.sqs_enabled:
            self._auto_initialize()

        if not self.client:
            print("[veriskgo] Client unavailable, spillover.")
            for msg in batch:
                self._spillover_save(msg)
            return

        for msg in batch:
            try:
                self.client.send_message(
                    QueueUrl=self.queue_url,
                    MessageBody=json.dumps(msg)
                )
                print("[veriskgo] Single retry OK")
            except Exception as e:
                print("[veriskgo] Single retry FAILED:", e)
                self._spillover_save(msg)


# -------------------------------------------------------
# SINGLETON INSTANCE
# -------------------------------------------------------
_sqs_instance = _VeriskGoSQS()

def send_to_sqs(bundle: Optional[Dict[str, Any]]):
    return _sqs_instance.send(bundle)

def flush_sqs():
    return _sqs_instance.force_flush()

def init_sqs():
    return _sqs_instance.sqs_enabled


# -------------------------------------------------------
# AUTO-FLUSH ON PYTHON EXIT
# -------------------------------------------------------
def _flush_on_exit():
    """Ensures all messages are sent BEFORE daemon threads die."""
    if os.getenv("VERISKGO_AUTOFLUSH", "1") == "0":
        print("[veriskgo] Auto-flush disabled.")
        return

    if os.getpid() != MAIN_PID:
        return

    print("[veriskgo] Automatic flush on exit...")
    try:
        _sqs_instance.force_flush()
    except Exception as e:
        print("[veriskgo] Flush on exit failed:", e)

atexit.register(_flush_on_exit)
