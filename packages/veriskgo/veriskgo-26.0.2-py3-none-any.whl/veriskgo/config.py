# src/veriskgo/config.py
import os 

def get_cfg():
    return {
        "aws_profile": os.getenv("AWS_PROFILE" , "sandbox"),
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "aws_sqs_url": os.getenv("AWS_SQS_URL") or "https://sqs.us-east-1.amazonaws.com/982135724133/otel-telemetry-queue",
        "env": os.getenv("ENV", "dev"),
        "project": os.getenv("PROJECT", "default-genai-app"),
    }
