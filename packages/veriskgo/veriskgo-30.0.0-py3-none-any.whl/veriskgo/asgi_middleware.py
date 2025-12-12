# veriskgo/asgi_middleware.py
import uuid
import time
import json
import os
import socket


from .trace_manager import TraceManager


class VeriskGOASGIMiddleware:

    def __init__(self, app, service_name="veriskgo_service"):
        self.app = app
        self.service_name = service_name

    def get_trace_name(self):
        project = os.path.basename(os.getcwd())
        hostname = socket.gethostname()

        return f"{project}_{hostname}"

    async def __call__(self, scope, receive, send):
        # We only trace HTTP traffic
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "UNKNOWN")

        # Extract user header (optional)
        headers = {k.decode(): v.decode() for k, v in scope.get("headers", [])}
        user_id = headers.get("x-user-id", "anonymous")
        session_id = headers.get("x-session-id", str(uuid.uuid4()))
        _name = self.get_trace_name()

        TraceManager.start_trace(
            _name,
            metadata={
                "path": path,
                "method": method,
                "user_id": user_id,
                "session_id": session_id,
            },
        )

        start_time = time.time()
        response_body = None

        async def send_wrapper(message):
            nonlocal response_body

            # Capture response body
            if message["type"] == "http.response.body":
                body = message.get("body")
                try:
                    response_body = body.decode() if body else None
                except Exception:
                    response_body = str(body)

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as exc:
            # Trace the exception
            TraceManager.finalize_and_send(
                user_id=user_id,
                session_id=session_id,
                trace_name="http_exception",
                trace_input={"path": path, "method": method},
                trace_output={"error": str(exc)},
            )
            raise

        # Normal completion
        TraceManager.finalize_and_send(
            user_id=user_id,
            session_id=session_id,
            trace_name=_name,
            trace_input={"path": path, "method": method},
            trace_output={
                "response": response_body,
                "latency_ms": int((time.time() - start_time) * 1000),
            },
        )
