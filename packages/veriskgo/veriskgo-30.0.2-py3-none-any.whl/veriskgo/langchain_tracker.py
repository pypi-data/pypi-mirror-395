# veriskgo/langchain_tracker.py

import time
import traceback
import functools
import inspect
import json

from veriskgo.trace_manager import TraceManager, serialize_value

 

# ------------------------------------------------------------
# CALLBACK TOKEN USAGE
# ------------------------------------------------------------

def _extract_lc_callback_usage(args, kwargs):
    usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

    def scan(obj):
        if obj is None:
            return

        if hasattr(obj, "prompt_tokens") or hasattr(obj, "completion_tokens"):
            usage["input_tokens"] = getattr(obj, "prompt_tokens", 0)
            usage["output_tokens"] = getattr(obj, "completion_tokens", 0)
            usage["total_tokens"] = getattr(
                obj,
                "total_tokens",
                usage["input_tokens"] + usage["output_tokens"],
            )
            return

        if isinstance(obj, dict):
            for v in obj.values():
                scan(v)

        if isinstance(obj, (list, tuple)):
            for v in obj:
                scan(v)

    scan(args)
    scan(kwargs)
    return usage

# ------------------------------------------------------------
# TEXT EXTRACTION (safe, no pylance errors)
# ------------------------------------------------------------

def _extract_lc_text(result):
    # Case 1: LC StrOutputParser returns str
    if isinstance(result, str):
        return result

    # Case 2: LC pipeline returns tuple like (summary, keywords)
    if isinstance(result, tuple) and len(result) >= 1:
        return result[0]

    # Case 3: ChatBedrock or LC Chat Models: check safely
    # (avoid hasattr(result, "content") for tuples/lists/dicts)
    if not isinstance(result, (str, dict, list, tuple)) and hasattr(result, "content"):
        return result.content

    # Case 4: Fallback — serialize it
    return serialize_value(result)



# ------------------------------------------------------------
# MODEL EXTRACTION
# ------------------------------------------------------------

def _extract_lc_model(result):
    meta = getattr(result, "response_metadata", None)
    if isinstance(meta, dict):
        return meta.get("model", None)
    return None


# ------------------------------------------------------------
# USAGE EXTRACTION
# ------------------------------------------------------------

def _extract_lc_usage(result, callback_usage):
    if callback_usage["total_tokens"] > 0:
        return callback_usage

    meta = getattr(result, "response_metadata", None)
    if isinstance(meta, dict):
        return {
            "input_tokens": meta.get("input_tokens", 0),
            "output_tokens": meta.get("output_tokens", 0),
            "total_tokens": meta.get("input_tokens", 0)
            + meta.get("output_tokens", 0),
        }

    return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


# ------------------------------------------------------------
# USAGE/COST PAIRS
# ------------------------------------------------------------

def _usage_pair(usage):
    return (
        {
            "input": usage["input_tokens"],
            "output": usage["output_tokens"],
            "total": usage["total_tokens"],
        },
        {
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
            "total_tokens": usage["total_tokens"],
        },
    )


def _calculate_cost(usage):
    PRICE_IN = 3.0 / 1_000_000
    PRICE_OUT = 15.0 / 1_000_000

    ic = round(usage["input_tokens"] * PRICE_IN, 6)
    oc = round(usage["output_tokens"] * PRICE_OUT, 6)
    total = round(ic + oc, 6)

    return (
        {"input": ic, "output": oc, "total": total},
        {"input_cost": ic, "output_cost": oc, "total_cost": total},
    )


# ------------------------------------------------------------
# MAIN DECORATOR
# ------------------------------------------------------------

def track_langchain(name: str = "langchain_call", *, tags: dict = {}):
    def decorator(func):

        is_async = inspect.iscoroutinefunction(func)

        # =====================================================
        # ASYNC WRAPPER
        # =====================================================
        async def async_wrapper(*args, **kwargs):

            if not TraceManager.has_active_trace():
                return await func(*args, **kwargs)

            # start the span
            span_id = TraceManager.start_span(
                name,
                input_data={"args": serialize_value(args),
                            "kwargs": serialize_value(kwargs)},
                tags=tags,
            )

            # ⭐ SET TYPE = "generation" (exact Bedrock logic)
            for sp in TraceManager._active["spans"]:
                if sp["span_id"] == span_id:
                    sp["type"] = "generation"

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

            callback_usage = _extract_lc_callback_usage(args, kwargs)
            usage = _extract_lc_usage(result, callback_usage)
            usage_details, usage_tokens = _usage_pair(usage)

            cost_details, cost_tokens = _calculate_cost(usage)

            model = _extract_lc_model(result)
            text = _extract_lc_text(result)

            # Build Langfuse-compatible LLM result
            generation_output = {
                "status": "success",
                "model": model,
                "latency_ms": latency,

                "input": {
                    "prompt": kwargs.get("prompt", None),
                    "model": model,
                    "messages": kwargs.get("messages", None),
                },

                "output": {
                    "text": text,
                    "finish_reason": getattr(result, "finish_reason", "stop"),
                },

                "usage_details": usage_details,
                "cost_details": cost_details,
                "usage": usage_tokens,
                "cost": cost_tokens,
            }

            TraceManager.end_span(
                span_id,
                {
                    "status": "success",
                    "model": model,
                    "latency_ms": latency,
                    "output": generation_output,
                    "duration_ms": latency,
                    "usage": usage_tokens,
                    "usage_details": usage_details,
                    "cost": cost_tokens,
                    "cost_details": cost_details,
                },
            )

            return result

        # =====================================================
        # SYNC WRAPPER
        # =====================================================
        def sync_wrapper(*args, **kwargs):

            if not TraceManager.has_active_trace():
                return func(*args, **kwargs)

            span_id = TraceManager.start_span(
                name,
                input_data={"args": serialize_value(args),
                            "kwargs": serialize_value(kwargs)},
                tags=tags,
            )

            # ⭐ SET TYPE = "generation"
            for sp in TraceManager._active["spans"]:
                if sp["span_id"] == span_id:
                    sp["type"] = "generation"

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

            callback_usage = _extract_lc_callback_usage(args, kwargs)
            usage = _extract_lc_usage(result, callback_usage)
            usage_details, usage_tokens = _usage_pair(usage)
            cost_details, cost_tokens = _calculate_cost(usage)

            model = _extract_lc_model(result)
            text = _extract_lc_text(result)

            generation_output = {
                "status": "success",
                "model": model,
                "latency_ms": latency,
                "input": {
                    "prompt": kwargs.get("prompt", None),
                    "model": model,
                    "messages": kwargs.get("messages", None),
                },
                "output": {
                    "text": text,
                    "finish_reason": getattr(result, "finish_reason", "stop"),
                },
                "usage_details": usage_details,
                "cost_details": cost_details,
                "usage": usage_tokens,
                "cost": cost_tokens,
            }

            TraceManager.end_span(
                span_id,
                {
                    "status": "success",
                    "model": model,
                    "latency_ms": latency,
                    "output": generation_output,
                    "duration_ms": latency,
                    "usage": usage_tokens,
                    "usage_details": usage_details,
                    "cost": cost_tokens,
                    "cost_details": cost_details,
                },
            )

            return result

        return functools.wraps(func)(async_wrapper if is_async else sync_wrapper)

    return decorator
