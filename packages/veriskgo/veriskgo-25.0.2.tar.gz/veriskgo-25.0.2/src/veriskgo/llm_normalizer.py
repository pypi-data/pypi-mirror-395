# veriskgo/llm_normalizer.py

def extract_text(resp: dict):
    """
    UNIVERSAL text extractor.
    Supports:
    - Bedrock Converse API
    - Bedrock InvokeModel API (Titan, Llama, Mistral)
    - Claude (Anthropic)
    - GPT (OpenAI)
    - Cohere
    - Mistral
    - Custom providers
    """
    if not isinstance(resp, dict):
        return str(resp)

    # 1. Bedrock Converse / Claude / Llama3 Chat
    try:
        return resp["output"]["message"]["content"][0]["text"]
    except Exception:
        pass

    # 2. Bedrock Claude Legacy
    try:
        return resp["content"][0]["text"]
    except Exception:
        pass

    # 3. Bedrock Titan Text
    try:
        return resp["results"][0]["outputText"]
    except Exception:
        pass

    # 4. Llama 3 Text / Mistral Text
    try:
        return resp["generation"]
    except Exception:
        pass

    # 5. Mistral (Mistral AI)
    try:
        return resp["outputs"][0]["text"]
    except Exception:
        pass

    # 6. Cohere Command
    try:
        return resp["text"]
    except Exception:
        pass

    # 7. OpenAI GPT-style
    try:
        return resp["choices"][0]["message"]["content"]
    except Exception:
        pass

    return str(resp)


def extract_usage(resp: dict):
    """
    UNIVERSAL usage/token extractor.
    Works across ALL Bedrock models + OpenAI + Anthropic.
    """
    usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
    }

    if not isinstance(resp, dict):
        return usage

    # Bedrock Converse (Claude / Llama3 Chat)
    if "usage" in resp:
        usage["input_tokens"] = resp["usage"].get("inputTokens", 0)
        usage["output_tokens"] = resp["usage"].get("outputTokens", 0)

    # Titan Text / Invoke Model
    if "results" in resp:
        usage["output_tokens"] = resp["results"][0].get("tokenCount", 0)

    # OpenAI GPT
    if "usage" in resp and "prompt_tokens" in resp["usage"]:
        usage["input_tokens"] = resp["usage"]["prompt_tokens"]
        usage["output_tokens"] = resp["usage"]["completion_tokens"]
        usage["total_tokens"] = resp["usage"]["total_tokens"]
        return usage

    usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"]
    return usage
