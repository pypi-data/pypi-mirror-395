# Legnext SDK Examples

This directory contains example scripts demonstrating various features of the Legnext Python SDK.

## Setup

1. Install the SDK:
   ```bash
   pip install legnext
   ```

2. Set your API key:
   ```bash
   export LEGNEXT_API_KEY="your-api-key-here"
   ```

3. For webhook examples, also set:
   ```bash
   export LEGNEXT_WEBHOOK_SECRET="your-webhook-secret"
   ```

## Examples

### Basic Examples

- **01_basic_generation.py** - Simple text-to-image generation
  ```bash
  python examples/01_basic_generation.py
  ```

- **02_async_generation.py** - Async/await pattern for concurrent operations
  ```bash
  python examples/02_async_generation.py
  ```

### Image Manipulation

- **03_image_variations.py** - Create variations, upscale, and reroll images
  ```bash
  python examples/03_image_variations.py
  ```

- **04_image_editing.py** - Pan, remix, edit, and remove backgrounds
  ```bash
  python examples/04_image_editing.py
  ```

### Video Generation

- **05_video_generation.py** - Generate, extend, and upscale videos
  ```bash
  python examples/05_video_generation.py
  ```

### Advanced Features

- **06_webhook_handler.py** - Handle webhook events from Legnext
  ```bash
  python examples/06_webhook_handler.py
  ```

## Common Patterns

### Error Handling

```python
from legnext import Client, LegnextAPIError, RateLimitError

client = Client(api_key="your-key")

try:
    response = client.midjourney.diffusion(text="a beautiful landscape")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
except LegnextAPIError as e:
    print(f"API error: {e.message} (status: {e.status_code})")
```

### Task Polling with Progress

```python
def show_progress(task):
    print(f"Status: {task.status}")
    if task.logs:
        print(f"Latest log: {task.logs[-1]}")

result = client.tasks.wait_for_completion(
    job_id="...",
    timeout=600,
    poll_interval=5,
    on_progress=show_progress
)
```

### Async Batch Processing

```python
import asyncio
from legnext import AsyncClient

async def generate_many(prompts):
    async with AsyncClient(api_key="your-key") as client:
        # Start all tasks
        tasks = [
            client.midjourney.diffusion(text=prompt)
            for prompt in prompts
        ]
        responses = await asyncio.gather(*tasks)

        # Wait for all to complete
        results = await asyncio.gather(*[
            client.tasks.wait_for_completion(r.job_id)
            for r in responses
        ])

        return results

# Generate 10 images concurrently
results = asyncio.run(generate_many([
    f"image prompt {i}" for i in range(10)
]))
```

## Support

For more information:
- [Official API Documentation](https://legnext.ai/docs)
- Email: support@legnext.cn
