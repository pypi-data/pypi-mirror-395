from __future__ import annotations
import uuid
import threading
import time
import traceback
import json
import sys
import inspect
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import functools

from .sqs import send_to_sqs

# ============================================================
# Safe Serialization Helpers
# ============================================================

def serialize_value(value: Any) -> Any:
    try:
        return json.loads(json.dumps(value, default=str))
    except Exception:
        return str(value)


def safe_locals(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: serialize_value(v) for k, v in d.items() if not k.startswith("_")}


# ============================================================
# Core Trace Manager
# ============================================================

class TraceManager:
    _lock = threading.Lock()

    _active: Dict[str, Any] = {
        "trace_id": None,
        "spans": [],
        "stack": [],
    }

    @classmethod
    def finalize_and_send(
        cls,
        *,
        user_id: str,
        session_id: str,
        trace_name: str,
        trace_input: dict,
        trace_output: dict,
        extra_spans: list = [],
    ):
        bundle = cls.end_trace()

        if not bundle:
            print("[VeriskGO] ERROR: No trace bundle was created.")
            return False

        if extra_spans:
            bundle["spans"].extend(extra_spans)

        bundle["user_id"] = user_id
        bundle["session_id"] = session_id
        bundle["trace_name"] = trace_name
        bundle["trace_input"] = trace_input
        bundle["trace_output"] = trace_output

        is_send = send_to_sqs(bundle)
        print(f"[VeriskGO] Trace sent: {is_send}\n")

        return True

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _id() -> str:
        return uuid.uuid4().hex

    # ---------------------------------------------------------
    # Trace API
    # ---------------------------------------------------------
    @classmethod
    def has_active_trace(cls) -> bool:
        return cls._active["trace_id"] is not None

    @classmethod
    def start_trace(cls, name: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        with cls._lock:
            trace_id = cls._id()
            root_id = cls._id()

            root_span = {
                "span_id": root_id,
                "parent_span_id": None,
                "name": name,
                "type": "root",
                "timestamp": cls._now(),
                "input": None,
                "output": None,
                "metadata": metadata or {},
                "duration_ms": 0,
            }

            cls._active["trace_id"] = trace_id
            cls._active["spans"] = [root_span]
            cls._active["stack"] = [{"span_id": root_id, "start": time.time()}]

            return trace_id

    @classmethod
    def end_trace(cls, final_output: Optional[Any] = None) -> Optional[Dict[str, Any]]:
        with cls._lock:
            if not cls._active["trace_id"]:
                return None

            while cls._active["stack"]:
                cls._end_current_span()

            if final_output:
                cls._active["spans"][0]["output"] = final_output

            bundle = {
                "trace_id": cls._active["trace_id"],
                "spans": cls._active["spans"].copy(),
            }

            cls._active["trace_id"] = None
            cls._active["spans"] = []
            cls._active["stack"] = []

            return bundle

    # ---------------------------------------------------------
    # Span API
    # ---------------------------------------------------------
    @classmethod
    def start_span(cls, name: str, input_data=None, tags=None):
        with cls._lock:
            if not cls._active["trace_id"]:
                return None

            parent = cls._active["stack"][-1]["span_id"]
            sid = cls._id()

            span = {
                "span_id": sid,
                "parent_span_id": parent,
                "name": name,
                "type": "child",
                "timestamp": cls._now(),
                "input": input_data,
                "metadata": tags or {},
                "output": None,
                "duration_ms": 0,
            }

            cls._active["spans"].append(span)
            cls._active["stack"].append({"span_id": sid, "start": time.time()})

            return sid

    @classmethod
    def end_span(cls, span_id: Optional[str], output_data=None):
        with cls._lock:
            if not cls._active["stack"]:
                return

            for i in reversed(range(len(cls._active["stack"]))):
                entry = cls._active["stack"][i]

                if entry["span_id"] == span_id:
                    duration = int((time.time() - entry["start"]) * 1000)
                    cls._active["stack"].pop(i)

                    for sp in cls._active["spans"]:
                        if sp["span_id"] == span_id:
                            sp["duration_ms"] = duration
                            sp["output"] = output_data

                            if isinstance(output_data, dict):
                                if "usage" in output_data:
                                    sp["usage"] = output_data["usage"]
                                if "usage_details" in output_data:
                                    sp["usage_details"] = output_data["usage_details"]
                                if "cost" in output_data:
                                    sp["cost"] = output_data["cost"]
                                if "cost_details" in output_data:
                                    sp["cost_details"] = output_data["cost_details"]

                            return

    @classmethod
    def _end_current_span(cls, output_data=None):
        entry = cls._active["stack"].pop()
        sid = entry["span_id"]
        duration = int((time.time() - entry["start"]) * 1000)

        for sp in cls._active["spans"]:
            if sp["span_id"] == sid:
                sp["duration_ms"] = duration
                if output_data:
                    sp["output"] = output_data

                    if isinstance(output_data, dict):
                        if "usage" in output_data:
                            sp["usage"] = output_data["usage"]
                        if "usage_details" in output_data:
                            sp["usage_details"] = output_data["usage_details"]
                        if "cost" in output_data:
                            sp["cost"] = output_data["cost"]
                        if "cost_details" in output_data:
                            sp["cost_details"] = output_data["cost_details"]

                return


# ============================================================
# Local Capture Utilities
# ============================================================

def capture_function_locals(func):
    locals_before = {}
    locals_after = {}

    target_code = func.__code__
    target_name = func.__name__
    target_module = func.__module__

    entered = False

    def tracer(frame, event, arg):
        nonlocal entered

        if frame.f_code is target_code and frame.f_globals.get("__name__") == target_module:

            if not entered:
                entered = True
                locals_before.update(safe_locals(frame.f_locals))

            if event == "return":
                locals_after.update(safe_locals(frame.f_locals))
                locals_after["_return"] = serialize_value(arg)

        return tracer

    return tracer, locals_before, locals_after


# ============================================================
# Decorator: track_function
# ============================================================

def track_function(name: Optional[str] = None, *, tags=None, capture_locals=True, capture_self=True):

    def decorator(func):

        span_name = name or func.__name__
        is_async = inspect.iscoroutinefunction(func)

        def sync_wrapper(*args, **kwargs):

            if not TraceManager.has_active_trace():
                return func(*args, **kwargs)

            span_id = TraceManager.start_span(
                span_name,
                input_data={"args": serialize_value(args), "kwargs": serialize_value(kwargs)},
                tags=tags,
            )

            start = time.time()

            tracer, locals_before, locals_after = capture_function_locals(func)
            sys.settrace(tracer)

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                sys.settrace(None)
                TraceManager.end_span(span_id, {
                    "status": "error",
                    "error": str(e),
                    "stacktrace": traceback.format_exc(),
                    "locals_before": locals_before,
                    "locals_after": locals_after,
                })
                raise

            sys.settrace(None)

            latency = int((time.time() - start) * 1000)

            TraceManager.end_span(span_id, {
                "status": "success",
                "latency_ms": latency,
                "locals_before": locals_before,
                "locals_after": locals_after,
                "output": serialize_value(result),
            })

            return result

        async def async_wrapper(*args, **kwargs):

            if not TraceManager.has_active_trace():
                return await func(*args, **kwargs)

            span_id = TraceManager.start_span(
                span_name,
                input_data={"args": serialize_value(args), "kwargs": serialize_value(kwargs)},
                tags=tags,
            )

            start = time.time()

            tracer, locals_before, locals_after = capture_function_locals(func)
            sys.settrace(tracer)

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                sys.settrace(None)
                TraceManager.end_span(span_id, {
                    "status": "error",
                    "error": str(e),
                    "stacktrace": traceback.format_exc(),
                    "locals_before": locals_before,
                    "locals_after": locals_after,
                })
                raise

            sys.settrace(None)

            latency = int((time.time() - start) * 1000)

            TraceManager.end_span(span_id, {
                "status": "success",
                "latency_ms": latency,
                "locals_before": locals_before,
                "locals_after": locals_after,
                "output": serialize_value(result),
            })
            return result

        return functools.wraps(func)(async_wrapper if is_async else sync_wrapper)

    return decorator


# ============================================================
# --------- COST + USAGE HELPERS (for Bedrock + LCEL) --------
# ============================================================

def calculate_cost(usage: dict):
    PRICE_IN = 3.0 / 1_000_000
    PRICE_OUT = 15.0 / 1_000_000

    ic = round(usage["input_tokens"] * PRICE_IN, 6)
    oc = round(usage["output_tokens"] * PRICE_OUT, 6)

    return {
        "input_cost": ic,
        "output_cost": oc,
        "total_cost": round(ic + oc, 6),
    }


def build_span_output(text_output, bedrock_response, model_id, latency):
    usage_raw = bedrock_response.get("usage", {})

    usage = {
        "input_tokens": usage_raw.get("inputTokens", 0),
        "output_tokens": usage_raw.get("outputTokens", 0),
        "total_tokens": usage_raw.get("inputTokens", 0)
                            + usage_raw.get("outputTokens", 0),
    }

    cost = calculate_cost(usage)

    return {
        "status": "success",
        "model": model_id,
        "latency_ms": latency,
        "output": {
            "text": text_output,
            "finish_reason": bedrock_response.get("stopReason")
        },
        "usage": usage,
        "usage_details": usage,
        "cost": cost,
        "cost_details": cost,
        "raw_bedrock_response": bedrock_response,
    }


# ============================================================
# -------- UNIVERSAL LLM DETAILS EXTRACTOR -------------------
# ============================================================

def extract_llm_details(func, result, model_id="", latency=0):
    """
    Works for:
      ✓ Raw Bedrock response (dict)
      ✓ LangChain ChatModel response (response_metadata)
      ✓ LCEL chain outputs (string)
      ✓ Tuple return: (text, raw_response)
      ✓ Plain text output
    """

    # 1. tuple → (text, response)
    if isinstance(result, tuple) and len(result) == 2:
        text_output, bedrock_response = result
        return build_span_output(text_output, bedrock_response, model_id, latency)

    # 2. Raw Bedrock dict
    if isinstance(result, dict) and "usage" in result:
        text_output = None
        try:
            text_output = result["output"]["message"]["content"][0]["text"]
        except:
            pass
        return build_span_output(text_output, result, model_id, latency)

    # 3. LangChain / LCEL with .response_metadata
    meta = getattr(result, "response_metadata", None)
    if isinstance(meta, dict):
        text_out = getattr(result, "content", None)

        usage = {
            "input_tokens": meta.get("input_tokens", 0),
            "output_tokens": meta.get("output_tokens", 0),
            "total_tokens": meta.get("input_tokens", 0)
                            + meta.get("output_tokens", 0),
        }

        cost = calculate_cost(usage)

        return {
            "status": "success",
            "model": model_id,
            "latency_ms": latency,
            "output": {"text": text_out},
            "usage": usage,
            "usage_details": usage,
            "cost": cost,
            "cost_details": cost,
        }

    # 4. Pure string
    if isinstance(result, str):
        return {
            "status": "success",
            "model": model_id,
            "latency_ms": latency,
            "output": {"text": result},
            "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            "cost": {"input_cost": 0, "output_cost": 0, "total_cost": 0},
        }

    # 5. Fallback output
    return {
        "status": "success",
        "model": model_id,
        "latency_ms": latency,
        "output": {"text": serialize_value(result)},
        "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
        "cost": {"input_cost": 0, "output_cost": 0, "total_cost": 0},
    }


# ============================================================
# ---------------- COMBINED LLM DECORATOR --------------------
# ============================================================

def track_llm_call(name: str = "llm_call", *, model_id: str = "", tags: dict = {}):
    """
    One decorator supporting:
      ✓ Sync Bedrock SDK calls
      ✓ Async LangChain chains
      ✓ ChatBedrock
      ✓ LCEL parser chains
      ✓ Text-only returns
      ✓ (text, response) tuples
    """

    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)

        async def async_wrapper(*args, **kwargs):

            if not TraceManager.has_active_trace():
                return await func(*args, **kwargs)

            span_id = TraceManager.start_span(
                name,
                input_data={
                    "args": serialize_value(args),
                    "kwargs": serialize_value(kwargs)
                },
                tags=tags,
            )

            start = time.time()

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                TraceManager.end_span(span_id, {
                    "status": "error",
                    "error": str(e),
                    "stacktrace": traceback.format_exc(),
                })
                raise

            latency = int((time.time() - start) * 1000)

            span_output = extract_llm_details(func, result, model_id=model_id, latency=latency)
            TraceManager.end_span(span_id, span_output)

            return result

        def sync_wrapper(*args, **kwargs):

            if not TraceManager.has_active_trace():
                return func(*args, **kwargs)

            span_id = TraceManager.start_span(
                name,
                input_data={
                    "args": serialize_value(args),
                    "kwargs": serialize_value(kwargs)
                },
                tags=tags,
            )

            start = time.time()

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                TraceManager.end_span(span_id, {
                    "status": "error",
                    "error": str(e),
                    "stacktrace": traceback.format_exc(),
                })
                raise

            latency = int((time.time() - start) * 1000)

            span_output = extract_llm_details(func, result, model_id=model_id, latency=latency)
            TraceManager.end_span(span_id, span_output)

            return result

        return functools.wraps(func)(async_wrapper if is_async else sync_wrapper)

    return decorator
