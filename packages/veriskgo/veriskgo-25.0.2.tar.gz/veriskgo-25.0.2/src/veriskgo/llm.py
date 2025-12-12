# veriskgo/llm.py
import time
import traceback
import functools
import inspect
from typing import Any, Dict, Optional

from veriskgo.trace_manager import TraceManager
from veriskgo.trace_manager import serialize_value

# ============================================================
# UNIVERSAL MODEL-AGNOSTIC NORMALIZERS
# ============================================================

def extract_text(resp: dict) -> str:
    """
    Extract model output text from ANY LLM:
    - Bedrock Converse API
    - Bedrock InvokeModel API (Titan / Llama text / Mistral text)
    - Anthropic
    - OpenAI
    - Cohere
    - Generic JSON
    """
    if not isinstance(resp, dict):
        return str(resp)

    try:
        return resp["output"]["message"]["content"][0]["text"]   # Bedrock Converse
    except Exception:
        pass

    try:
        return resp["content"][0]["text"]  # Bedrock Claude legacy
    except Exception:
        pass

    try:
        return resp["results"][0]["outputText"]  # Titan
    except Exception:
        pass

    try:
        return resp["generation"]  # Llama / Mistral text
    except Exception:
        pass

    try:
        return resp["outputs"][0]["text"]  # Mistral AI
    except Exception:
        pass

    try:
        return resp["text"]  # Cohere
    except Exception:
        pass

    try:
        return resp["choices"][0]["message"]["content"]  # OpenAI GPT
    except Exception:
        pass

    return str(resp)


def extract_usage(resp: dict) -> Dict[str, int]:
    """Normalize token usage across all model providers."""
    usage = {"input": 0, "output": 0, "total": 0}

    if not isinstance(resp, dict):
        return usage

    if "usage" in resp:
        usage["input"] = resp["usage"].get("inputTokens", 0)
        usage["output"] = resp["usage"].get("outputTokens", 0)

    if "results" in resp:
        usage["output"] = resp["results"][0].get("tokenCount", usage["output"])

    if "usage" in resp and "prompt_tokens" in resp["usage"]:
        usage["input"] = resp["usage"]["prompt_tokens"]
        usage["output"] = resp["usage"]["completion_tokens"]
        usage["total"] = resp["usage"]["total_tokens"]
        return usage

    usage["total"] = usage["input"] + usage["output"]
    return usage


# ============================================================
# Decorator: track_llm_call (Generation Span)
# ============================================================

def track_llm_call(name=None, tags=None):
    """
    Wraps an LLM call inside a Langfuse-compatible 'generation' span.
    Supports BOTH sync and async LLM functions.
    NEVER modifies the user function's return value.
    """

    def decorator(func):
        span_name = name or func.__name__
        is_async = inspect.iscoroutinefunction(func)

        # =====================================================================
        # SHARED PARSE FUNCTION
        # =====================================================================
        def parse_for_tracing(resp):
            text = extract_text(resp)
            usage = extract_usage(resp)

            input_tokens = usage["input"]
            output_tokens = usage["output"]
            total_tokens = usage["total"]

            input_cost = input_tokens * 0.0000015
            output_cost = output_tokens * 0.000005

            return {
                "text": text,
                "usage_details": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": total_tokens,
                },
                "cost_details": {
                    "input": round(input_cost, 6),
                    "output": round(output_cost, 6),
                    "total": round(input_cost + output_cost, 6),
                },
            }

        # =====================================================================
        # SYNC WRAPPER
        # =====================================================================
        def sync_wrapper(*args, **kwargs):
            prompt_value = None
            for a in args:
                if isinstance(a, str):
                    prompt_value = a
                    break
 

            span_id = TraceManager.start_span(
                span_name,
                input_data={"prompt": prompt_value, "tags": tags},
                tags=tags,
            )

            # mark this span as generation
            for sp in TraceManager._active["spans"]:
                if sp["span_id"] == span_id:
                    sp["type"] = "generation"

            start = time.time()

            try:
                resp = func(*args, **kwargs)  # ORIGINAL RETURN VALUE
                latency = int((end := time.time()) - start) * 1000

                parsed = parse_for_tracing(resp)

                TraceManager.end_span(
                    span_id,
                    {
                        "status": "success",
                        "model": resp.get("model") if isinstance(resp, dict) else None,
                        "latency_ms": latency,
                        "input": {
                            "prompt": prompt_value,
                            "model": resp.get("model") if isinstance(resp, dict) else None,
                            "messages": resp.get("messages") if isinstance(resp, dict) else None,
                        },
                        "output": {
                            "text": parsed["text"],
                            "finish_reason": "stop",
                        },
                        "usage_details": parsed["usage_details"],
                        "cost_details": parsed["cost_details"],
                        "usage": {
                            "input_tokens": parsed["usage_details"]["input"],
                            "output_tokens": parsed["usage_details"]["output"],
                            "total_tokens": parsed["usage_details"]["total"],
                        },
                        "cost": {
                            "input_cost": parsed["cost_details"]["input"],
                            "output_cost": parsed["cost_details"]["output"],
                            "total_cost": parsed["cost_details"]["total"],
                        },
                    },
                )

                return resp  # <-- RETURN ORIGINAL VALUE

            except Exception as e:
                latency = int((time.time() - start) * 1000)

                TraceManager.end_span(
                    span_id,
                    {
                        "status": "error",
                        "error": str(e),
                        "stacktrace": traceback.format_exc(),
                        "latency_ms": latency,
                    },
                )
                raise

        # =====================================================================
        # ASYNC WRAPPER
        # =====================================================================
        async def async_wrapper(*args, **kwargs):
            prompt_value = None
            for a in args:
                if isinstance(a, str):
                    prompt_value = a
                    break


            span_id = TraceManager.start_span(
                span_name,
                input_data={"prompt": prompt_value, "tags": tags},
                tags=tags,
            )

            for sp in TraceManager._active["spans"]:
                if sp["span_id"] == span_id:
                    sp["type"] = "generation"

            start = time.time()

            try:
                resp = await func(*args, **kwargs)  # ORIGINAL OUTPUT
                latency = int((time.time() - start) * 1000)

                parsed = parse_for_tracing(resp)

                TraceManager.end_span(
                    span_id,
                    {
                        "status": "success",
                        "model": resp.get("model") if isinstance(resp, dict) else None,
                        "latency_ms": latency,
                        "input": {
                            "prompt": prompt_value,
                            "model": resp.get("model") if isinstance(resp, dict) else None,
                            "messages": resp.get("messages") if isinstance(resp, dict) else None,
                        },

                        "output": {
                            "text": parsed["text"],
                            "finish_reason": "stop",
                        },
                        "usage_details": parsed["usage_details"],
                        "cost_details": parsed["cost_details"],
                        "usage": {
                            "input_tokens": parsed["usage_details"]["input"],
                            "output_tokens": parsed["usage_details"]["output"],
                            "total_tokens": parsed["usage_details"]["total"],
                        },
                        "cost": {
                            "input_cost": parsed["cost_details"]["input"],
                            "output_cost": parsed["cost_details"]["output"],
                            "total_cost": parsed["cost_details"]["total"],
                        },
                    },
                )

                return resp  # <-- RETURN ORIGINAL VALUE

            except Exception as e:
                latency = int((time.time() - start) * 1000)

                TraceManager.end_span(
                    span_id,
                    {
                        "status": "error",
                        "error": str(e),
                        "stacktrace": traceback.format_exc(),
                        "latency_ms": latency,
                    },
                )
                raise

        return functools.wraps(func)(async_wrapper if is_async else sync_wrapper)

    return decorator


# ============================================================
# Helper for LLM Response Processing (legacy)
# ============================================================

def _process_llm_response(prompt: str, response: Dict[str, Any], latency_ms: int):
    """
    Backward-compatible helper. 
    Uses universal extractors but does not modify app behavior.
    """
    text = extract_text(response)
    usage = extract_usage(response)

    input_tokens = usage["input"]
    output_tokens = usage["output"]
    total_tokens = usage["total"]

    input_cost = input_tokens * 0.0000015
    output_cost = output_tokens * 0.000005
    total_cost = input_cost + output_cost

    model = response.get("model", "unknown") if isinstance(response, dict) else "unknown"

    return {
        "status": "success",
        "type": "generation",
        "latency_ms": latency_ms,
        "input": {
            "prompt": prompt,
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        "output": {
            "text": text,
            "finish_reason": "stop",
        },
        "usage_details": {
            "input": input_tokens,
            "output": output_tokens,
            "total": total_tokens,
        },
        "cost_details": {
            "input": round(input_cost, 6),
            "output": round(output_cost, 6),
            "total": round(total_cost, 6),
        },
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "cost": {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6),
        },
        "raw_response": serialize_value(response),
    }
