# veriskgo/cli_doctor.py

import sys
import os
import importlib.util
import uuid
from veriskgo.sqs import init_sqs, SPILLOVER_FILE
from veriskgo.config import get_cfg
from veriskgo.trace_manager import TraceManager, serialize_value   # NEW
import time
def check_dependency(module: str) -> bool:
    """Return True if a module exists without importing it."""
    return importlib.util.find_spec(module) is not None


def check_python():
    version = sys.version.split()[0]
    major = sys.version_info.major
    minor = sys.version_info.minor
    ok = (major >= 3 and minor >= 10)
    return ok, f"Python {version}"


def check_veriskgo_installed():
    try:
        import veriskgo
        version = getattr(veriskgo, "__version__", None)

        if version:
            return True, f"veriskgo version {version}"
        else:
            return True, "veriskgo installed (version unknown)"

    except ImportError:
        return False, "veriskgo not importable"



def check_aws_credentials():
    if not check_dependency("boto3"):
        return False, "boto3 missing (required for AWS checks)"

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
        return False, f"AWS credential check failed: {str(e)}"


def check_sqs_connectivity():
    if not check_dependency("boto3"):
        return False, "boto3 missing → cannot test SQS connectivity"

    if not init_sqs():
        return False, "SQS client not configured/not reachable"

    return True, "SQS connectivity OK"


def check_spillover_path():
    try:
        path = SPILLOVER_FILE
        base = os.path.dirname(path)
        if not os.path.exists(base):
            return False, f"Spillover directory missing: {base}"
        return True, f"Spillover file path OK: {path}"
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

        ("boto3 (for SQS)",
            lambda: check_optional_dependency("boto3", "SQS Telemetry", "pip install boto3")),
        ("requests (for HTTP calls)",
            lambda: check_optional_dependency("requests", "API features", "pip install requests")),
    ]

    failed = 0
    results_dict = {}     # <-- To collect results for SQS trace

    for label, func in checks:
        try:
            ok, msg = func()
        except Exception as e:
            ok = False
            msg = str(e)

        results_dict[label] = {
            "ok": ok,
            "message": msg,
        }

        status = "✔" if ok else "✖"
        print(f"{status} {label}: {msg}")

        if not ok:
            failed += 1

    print("\n-----------------------------------")

    if failed == 0:
        print("🎉 All checks passed. Your VeriskGO environment is healthy!\n")
    else:
        print(f"⚠ {failed} issue(s) detected.")
        print("Fix the above items before using full VeriskGO functionality.\n")

    # -----------------------------------------------------------------
    # NEW: Send a doctor trace to SQS
    # -----------------------------------------------------------------
    try:
        TraceManager.start_trace("veriskgo_doctor_trace")
        time.sleep(10)

        TraceManager.finalize_and_send(
            user_id="doctor",
            session_id=uuid.uuid4().hex,
            trace_name="veriskgo_doctor",
            trace_input={"checks": "environment-diagnostics"},
            trace_output=serialize_value(results_dict),
        )

        print("📨 Doctor trace sent to SQS.\n")

    except Exception as e:
        print(f"⚠ Failed to send doctor trace to SQS: {e}\n")
