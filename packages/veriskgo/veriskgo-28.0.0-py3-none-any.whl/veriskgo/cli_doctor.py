# veriskgo/cli_doctor.py

import sys
import os
import importlib.util
import uuid

from .sqs import init_sqs, SPILLOVER_FILE, _sqs_instance
from .config import get_cfg
from .trace_manager import TraceManager, serialize_value
import json

def check_dependency(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def check_python():
    version = sys.version.split()[0]
    ok = sys.version_info >= (3, 10)
    return ok, f"Python {version}"


def check_veriskgo_installed():
    try:
        from . import __version__ as veriskgo_version

        if veriskgo_version and veriskgo_version != "0.0.0":
            return True, f"veriskgo version {veriskgo_version}"
        else:
            return True, "veriskgo installed (local source, version unknown)"

    except Exception:
        return False, "veriskgo not importable"


def check_aws_credentials():
    if not check_dependency("boto3"):
        return False, "boto3 missing"

    import boto3
    try:
        cfg = get_cfg()
        session = boto3.Session(
            profile_name=cfg.get("aws_profile"),
            region_name=cfg.get("aws_region", "us-east-1")
        )
        sts = session.client("sts")
        ident = sts.get_caller_identity()
        return True, f"AWS Credentials OK (UserId={ident['UserId']})"
    except Exception as e:
        return False, f"Failed: {str(e)}"


def check_sqs_connectivity():
    if not check_dependency("boto3"):
        return False, "boto3 missing"

    if not init_sqs():
        return False, "SQS client not reachable"

    return True, "SQS connectivity OK"


def check_spillover_path():
    try:
        base = os.path.dirname(SPILLOVER_FILE)
        if not os.path.exists(base):
            return False, f"Missing directory: {base}"
        return True, f"Path OK: {SPILLOVER_FILE}"
    except Exception as e:
        return False, str(e)


def check_optional_dependency(module, feature, install_cmd):
    installed = check_dependency(module)
    if installed:
        return True, f"{module} installed (for {feature})"
    return False, f"{module} missing → install: {install_cmd}"


def run_doctor():
    print("\n🔍 VeriskGO Doctor — System Diagnostics\n")

    checks = [
        ("Python version", check_python),
        ("veriskgo installed", check_veriskgo_installed),
        ("AWS Credentials", check_aws_credentials),
        ("SQS Connectivity", check_sqs_connectivity),
        ("Spillover path", check_spillover_path),
        ("boto3 (for SQS)", lambda: check_optional_dependency("boto3", "SQS", "pip install boto3")),
    ]

    failed = 0
    results_dict = {}

    for label, func in checks:
        ok, msg = func()
        results_dict[label] = {"ok": ok, "message": msg}

        print(("✔ " if ok else "✖ ") + f"{label}: {msg}")

        if not ok:
            failed += 1

    print("\n-----------------------------------")
    if failed == 0:
        print("🎉 All checks passed. Your VeriskGO environment is healthy!\n")
    else:
        print(f"⚠ {failed} issue(s) detected.\n")

    # ---------------------------------------------------------
    # SEND DOCTOR TRACE — FULLY SYNCHRONOUS + SAFE
    # ---------------------------------------------------------
    try:
        TraceManager.start_trace("veriskgo_doctor_trace")

        bundle = TraceManager.end_trace({"health": "diagnostics"})

        # If bundle is None → trace did not start correctly
        if not bundle:
            print("⚠ No trace bundle created → doctor trace not sent.\n")
            return

        # Attach additional data
        bundle["user_id"] = "doctor"
        bundle["session_id"] = uuid.uuid4().hex
        bundle["trace_name"] = "veriskgo_doctor"
        bundle["trace_input"] = {"checks": "environment"}
        bundle["trace_output"] = serialize_value(results_dict)

        # Ensure SQS is initialized
        if not init_sqs():
            print("⚠ SQS not initialized → cannot send doctor trace.\n")
            return

        client = _sqs_instance.client
        url = _sqs_instance.queue_url

        if not client or not url:
            print("⚠ Doctor trace SQS client missing.\n")
            return

        # ⭐ Fully synchronous send
        client.send_message(
            QueueUrl=url,
            MessageBody=json.dumps(bundle)
        )

        print("📨 Doctor trace sent to SQS.\n")

    except Exception as e:
        print(f"⚠ Failed to send doctor trace to SQS: {e}\n")
