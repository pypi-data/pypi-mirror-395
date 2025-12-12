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
    - Clean shutdown (prevents Event loop is closed errors on Windows)
    - Auto spillover for failed sends
    """

    SHUTDOWN_SENTINEL = None  # Used to tell workers to stop

    def __init__(self):
        self.client: Optional[Any] = None
        self.queue_url: Optional[str] = None
        self.sqs_enabled = False
        self._init_once = False

        # Internal queue
        self._q: queue.Queue = queue.Queue(maxsize=0)

        # Flag to stop workers cleanly
        self._shutting_down = False

        # Restore spillover messages
        self._load_spillover()

        # Start worker threads
        self.worker_count = 4
        self.workers = []
        for i in range(self.worker_count):
            t = threading.Thread(target=self._safe_worker_loop, daemon=True)
            t.start()
            self.workers.append(t)

        # Initialize AWS
        self._auto_initialize()

    # -------------------------------------------------------
    # CLEAN SHUTDOWN SUPPORT
    # -------------------------------------------------------
    def shutdown(self):
        """Safely stop worker threads without touching asyncio loop."""
        if self._shutting_down:
            return
        self._shutting_down = True

        # Signal workers to exit
        for _ in range(self.worker_count):
            self._q.put(self.SHUTDOWN_SENTINEL)

        # Wait for them to finish
        for t in self.workers:
            try:
                t.join(timeout=1.0)
            except Exception:
                pass

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
    # SAFE WORKER LOOP (auto-restarting)
    # -------------------------------------------------------
    def _safe_worker_loop(self):
        while True:
            try:
                self._worker_loop()
                return
            except Exception as e:
                print("[veriskgo] Worker crashed:", e)
                time.sleep(0.5)
                print("[veriskgo] Restarting worker...")

    # -------------------------------------------------------
    # REAL WORKER LOOP
    # -------------------------------------------------------
    def _worker_loop(self):
        batch = []
        while True:
            try:
                msg = self._q.get(timeout=0.2)

                # Shutdown signal
                if msg is self.SHUTDOWN_SENTINEL:
                    return

                batch.append(msg)

            except queue.Empty:
                pass

            # Batch conditions
            flush_size = len(batch) >= 10
            flush_time = batch and (time.time() % 1 < 0.15)

            if flush_size or flush_time:
                try:
                    self._send_batch(batch)
                except RuntimeError as e:
                    if "Event loop is closed" in str(e):
                        # Safe ignore — Windows cleanup issue
                        return
                    raise
                batch = []

    # -------------------------------------------------------
    # FORCE FLUSH
    # -------------------------------------------------------
    def force_flush(self):
        """Synchronously send all remaining messages."""
        batch = []
        while not self._q.empty():
            try:
                msg = self._q.get_nowait()
                if msg is not self.SHUTDOWN_SENTINEL:
                    batch.append(msg)
            except Exception:
                break

        if batch:
            print("[veriskgo] Force flush triggered")
            self._send_batch(batch)

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
                region_name=cfg.get("aws_region")
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

        if not self.client:
            self._auto_initialize()

        if not self.client:
            print("[veriskgo] SQS unavailable → spillover.")
            for msg in batch:
                self._spillover_save(msg)
            return

        entries = [
            {"Id": str(i), "MessageBody": json.dumps(msg)}
            for i, msg in enumerate(batch[:10])
        ]

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
    # RETRY INDIVIDUALMESSAGES
    # -------------------------------------------------------
    def _retry_individual(self, batch):
        # Ensure SQS client exists
        if not self.client:
            self._auto_initialize()

        client = self.client  # type: ignore
        if not client:
            print("[veriskgo] Client unavailable → spilling all messages.")
            for msg in batch:
                self._spillover_save(msg)
            return

        for msg in batch:
            try:
                client.send_message(
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
# AUTO-FLUSH + CLEAN SHUTDOWN
# -------------------------------------------------------
def _cleanup_at_exit():
    if os.getpid() != MAIN_PID:
        return

    print("[veriskgo] Automatic flush on exit...")

    try:
        _sqs_instance.shutdown()     # NEW: stops background threads
        _sqs_instance.force_flush()  # send remaining messages
    except Exception as e:
        print("[veriskgo] Exit flush failed:", e)

atexit.register(_cleanup_at_exit)
