"""Tests for webhook functionality."""

import hashlib
import hmac
import json

import pytest

from legnext.webhook import WebhookHandler, WebhookVerifier


def test_webhook_verifier():
    """Test webhook signature verification."""
    secret = "test_secret"
    verifier = WebhookVerifier(secret)

    payload = b'{"test": "data"}'
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    assert verifier.verify(payload, signature) is True
    assert verifier.verify(payload, "invalid_signature") is False


def test_webhook_verifier_with_timestamp():
    """Test webhook verification with timestamp."""
    secret = "test_secret"
    verifier = WebhookVerifier(secret)

    payload = b'{"test": "data"}'
    timestamp = "1234567890"
    signed_payload = f"{timestamp}.".encode() + payload
    signature = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()

    assert verifier.verify(payload, signature, timestamp) is True


def test_webhook_handler_registration():
    """Test webhook handler event registration."""
    handler = WebhookHandler("secret")

    @handler.on_completed
    def test_completed(task):
        pass

    @handler.on_failed
    def test_failed(task):
        pass

    assert len(handler._handlers["completed"]) == 1
    assert len(handler._handlers["failed"]) == 1


def test_webhook_handler_execution(mock_task_response):
    """Test webhook handler execution."""
    handler = WebhookHandler("secret")
    completed_called = []

    @handler.on_completed
    def handle_completed(task):
        completed_called.append(task.job_id)

    # Create valid signature
    payload = json.dumps(mock_task_response).encode()
    signature = hmac.new("secret".encode(), payload, hashlib.sha256).hexdigest()

    # Handle the webhook
    handler.handle(payload, signature)

    assert len(completed_called) == 1
    assert completed_called[0] == mock_task_response["job_id"]


def test_webhook_handler_invalid_signature(mock_task_response):
    """Test webhook handler with invalid signature."""
    handler = WebhookHandler("secret")
    payload = json.dumps(mock_task_response).encode()

    with pytest.raises(ValueError, match="Invalid webhook signature"):
        handler.handle(payload, "invalid_signature")


def test_webhook_handler_any_event(mock_task_response):
    """Test webhook handler 'any' event."""
    handler = WebhookHandler("secret")
    any_called = []

    @handler.on_any
    def handle_any(task):
        any_called.append(task.job_id)

    payload = json.dumps(mock_task_response).encode()
    signature = hmac.new("secret".encode(), payload, hashlib.sha256).hexdigest()

    handler.handle(payload, signature)

    assert len(any_called) == 1
