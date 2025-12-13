"""Webhook handler example."""

import os

from legnext.webhook import WebhookHandler, create_webhook_server

# Initialize the webhook handler
handler = WebhookHandler(webhook_secret=os.environ.get("LEGNEXT_WEBHOOK_SECRET", "your-secret"))


# Register handlers for different events
@handler.on_completed
def handle_completed(task):
    """Handle completed tasks."""
    print(f"Task {task.job_id} completed!")
    print(f"Task type: {task.task_type}")
    if task.output and task.output.image_urls:
        print(f"Generated {len(task.output.image_urls)} images")
        for i, url in enumerate(task.output.image_urls, 1):
            print(f"  Image {i}: {url}")


@handler.on_failed
def handle_failed(task):
    """Handle failed tasks."""
    print(f"Task {task.job_id} failed!")
    if task.error:
        print(f"Error: {task.error.message}")


@handler.on_processing
def handle_processing(task):
    """Handle processing updates."""
    print(f"Task {task.job_id} is now processing...")


@handler.on_any
def log_all_events(task):
    """Log all events for debugging."""
    print(f"[LOG] Task {task.job_id}: {task.status}")


# Option 1: Use the built-in simple server (for testing)
if __name__ == "__main__":
    print("Starting webhook server...")
    print("Configure your webhook URL: http://your-server:8000/webhook")
    create_webhook_server(handler, port=8000)

# Option 2: Use with Flask
"""
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        handler.handle(
            payload=request.get_data(),
            signature=request.headers.get("X-Legnext-Signature", ""),
            timestamp=request.headers.get("X-Legnext-Timestamp"),
        )
        return {"status": "ok"}
    except ValueError as e:
        return {"error": str(e)}, 401

if __name__ == "__main__":
    app.run(port=8000)
"""

# Option 3: Use with FastAPI
"""
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.body()
        signature = request.headers.get("x-legnext-signature", "")
        timestamp = request.headers.get("x-legnext-timestamp")

        handler.handle(
            payload=body,
            signature=signature,
            timestamp=timestamp,
        )
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
