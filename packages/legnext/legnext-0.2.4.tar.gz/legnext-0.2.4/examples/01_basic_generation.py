"""Basic image generation example."""

import os

from legnext import Client

# Initialize the client
client = Client(api_key=os.environ.get("LEGNEXT_API_KEY"))

# Generate an image
print("Generating image...")
response = client.midjourney.diffusion(
    text="a beautiful sunset over mountains, photorealistic"
)

print(f"Job ID: {response.job_id}")
print(f"Status: {response.status}")

# Wait for completion
print("\nWaiting for completion...")


def progress_callback(task):
    print(f"  Status: {task.status}")


result = client.tasks.wait_for_completion(response.job_id, on_progress=progress_callback)

# Print results
print("\nCompleted!")
print(f"Generated {len(result.output.image_urls)} images:")
for i, url in enumerate(result.output.image_urls, 1):
    print(f"  Image {i}: {url}")

if result.output.seed:
    print(f"\nSeed (for reproducibility): {result.output.seed}")
