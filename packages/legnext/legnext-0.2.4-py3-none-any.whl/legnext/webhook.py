"""Webhook utilities for the Legnext SDK."""

import hashlib
import hmac
from typing import Any, Callable, Dict, Optional

from legnext.types.responses import TaskResponse


class WebhookVerifier:
    """Verify webhook signatures from Legnext."""

    def __init__(self, webhook_secret: str) -> None:
        """Initialize the webhook verifier.

        Args:
            webhook_secret: The webhook secret configured in your Legnext webhook settings
        """
        self.webhook_secret = webhook_secret.encode("utf-8")

    def verify(
        self,
        payload: bytes,
        signature: str,
        timestamp: Optional[str] = None,
    ) -> bool:
        """Verify a webhook signature.

        Args:
            payload: Raw request body as bytes
            signature: Signature from the webhook header
            timestamp: Optional timestamp from webhook header

        Returns:
            True if signature is valid, False otherwise

        Example:
            ```python
            verifier = WebhookVerifier(webhook_secret="your-secret")

            # In your webhook handler
            is_valid = verifier.verify(
                payload=request.body,
                signature=request.headers["X-Legnext-Signature"]
            )

            if not is_valid:
                return {"error": "Invalid signature"}, 401
            ```
        """
        # Construct the signed payload
        if timestamp:
            signed_payload = f"{timestamp}.".encode("utf-8") + payload
        else:
            signed_payload = payload

        # Calculate HMAC
        expected_signature = hmac.new(
            self.webhook_secret, signed_payload, hashlib.sha256
        ).hexdigest()

        # Compare signatures (constant-time comparison to prevent timing attacks)
        return hmac.compare_digest(expected_signature, signature)


class WebhookHandler:
    """Handle webhook events from Legnext.

    Example:
        ```python
        from legnext.webhook import WebhookHandler
        from legnext.types import JobStatus

        handler = WebhookHandler(webhook_secret="your-secret")

        @handler.on_completed
        def handle_completed(task):
            print(f"Task {task.job_id} completed!")
            print(f"Results: {task.output.image_urls}")

        @handler.on_failed
        def handle_failed(task):
            print(f"Task {task.job_id} failed: {task.error.message}")

        # In your webhook endpoint
        @app.post("/webhook")
        def webhook(request):
            handler.handle(
                payload=request.body,
                signature=request.headers["X-Legnext-Signature"]
            )
            return {"status": "ok"}
        ```
    """

    def __init__(self, webhook_secret: str) -> None:
        """Initialize the webhook handler.

        Args:
            webhook_secret: The webhook secret configured in your Legnext webhook settings
        """
        self.verifier = WebhookVerifier(webhook_secret)
        self._handlers: Dict[str, list[Callable[[TaskResponse], Any]]] = {
            "completed": [],
            "failed": [],
            "processing": [],
            "any": [],
        }

    def on_completed(self, func: Callable[[TaskResponse], Any]) -> Callable[[TaskResponse], Any]:
        """Register a handler for completed tasks.

        Args:
            func: Function to call when a task completes

        Returns:
            The decorated function
        """
        self._handlers["completed"].append(func)
        return func

    def on_failed(self, func: Callable[[TaskResponse], Any]) -> Callable[[TaskResponse], Any]:
        """Register a handler for failed tasks.

        Args:
            func: Function to call when a task fails

        Returns:
            The decorated function
        """
        self._handlers["failed"].append(func)
        return func

    def on_processing(self, func: Callable[[TaskResponse], Any]) -> Callable[[TaskResponse], Any]:
        """Register a handler for processing status updates.

        Args:
            func: Function to call when a task starts processing

        Returns:
            The decorated function
        """
        self._handlers["processing"].append(func)
        return func

    def on_any(self, func: Callable[[TaskResponse], Any]) -> Callable[[TaskResponse], Any]:
        """Register a handler for any task status.

        Args:
            func: Function to call for any task update

        Returns:
            The decorated function
        """
        self._handlers["any"].append(func)
        return func

    def handle(
        self,
        payload: bytes,
        signature: str,
        timestamp: Optional[str] = None,
        verify_signature: bool = True,
    ) -> None:
        """Handle a webhook event.

        Args:
            payload: Raw request body as bytes
            signature: Signature from the webhook header
            timestamp: Optional timestamp from webhook header
            verify_signature: Whether to verify the signature (default: True)

        Raises:
            ValueError: If signature verification fails
        """
        # Verify signature
        if verify_signature:
            if not self.verifier.verify(payload, signature, timestamp):
                raise ValueError("Invalid webhook signature")

        # Parse payload
        import json

        data = json.loads(payload.decode("utf-8"))
        task = TaskResponse.model_validate(data)

        # Call handlers
        status_key = task.status.value
        if status_key in self._handlers:
            for handler in self._handlers[status_key]:
                handler(task)

        # Call "any" handlers
        for handler in self._handlers["any"]:
            handler(task)


def create_webhook_server(
    handler: WebhookHandler,
    host: str = "0.0.0.0",
    port: int = 8000,
    path: str = "/webhook",
) -> None:
    """Create a simple webhook server for testing.

    This is a convenience function for development/testing. In production,
    use your preferred web framework (Flask, FastAPI, Django, etc.).

    Args:
        handler: WebhookHandler instance
        host: Host to bind to
        port: Port to listen on
        path: URL path for the webhook endpoint

    Example:
        ```python
        from legnext.webhook import WebhookHandler, create_webhook_server

        handler = WebhookHandler(webhook_secret="your-secret")

        @handler.on_completed
        def handle_completed(task):
            print(f"Task completed: {task.job_id}")

        create_webhook_server(handler, port=8000)
        ```
    """
    try:
        from http.server import BaseHTTPRequestHandler, HTTPServer
    except ImportError as e:
        raise ImportError("Standard library http.server required for webhook server") from e

    class WebhookRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            if self.path != path:
                self.send_response(404)
                self.end_headers()
                return

            # Read payload
            content_length = int(self.headers.get("Content-Length", 0))
            payload = self.rfile.read(content_length)

            # Get signature
            signature = self.headers.get("X-Legnext-Signature", "")
            timestamp = self.headers.get("X-Legnext-Timestamp")

            try:
                handler.handle(payload, signature, timestamp)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except ValueError as e:
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())

        def log_message(self, format: str, *args: Any) -> None:
            # Custom logging
            print(f"[Webhook] {format % args}")

    server = HTTPServer((host, port), WebhookRequestHandler)
    print(f"Webhook server listening on http://{host}:{port}{path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down webhook server...")
        server.shutdown()
