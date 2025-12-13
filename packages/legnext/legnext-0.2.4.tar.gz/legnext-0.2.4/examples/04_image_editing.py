"""Image editing operations example."""

import os

from legnext import Client

client = Client(api_key=os.environ.get("LEGNEXT_API_KEY"))

# Generate initial image
print("1. Generating initial image...")
response = client.midjourney.diffusion(text="a modern house exterior, architecture photography")
result = client.tasks.wait_for_completion(response.job_id)
job_id = result.job_id
print(f"Generated: {job_id}")

# Pan/extend the image
print("\n2. Panning right...")
pan = client.midjourney.pan(job_id=job_id, image_no=0, direction="right")
pan_result = client.tasks.wait_for_completion(pan.job_id)
print(f"Extended: {pan_result.output.image_url}")

# Remix with a new prompt
print("\n3. Remixing with new style...")
remix = client.midjourney.remix(
    job_id=job_id, image_no=0, prompt="make it a victorian style house", intensity=0.7
)
remix_result = client.tasks.wait_for_completion(remix.job_id)
print(f"Remixed: {remix_result.output.image_url}")

# Edit specific region
print("\n4. Editing region...")
edit = client.midjourney.edit(
    job_id=job_id, image_no=0, prompt="add a beautiful garden in front"
)
edit_result = client.tasks.wait_for_completion(edit.job_id)
print(f"Region edited: {edit_result.output.image_url}")

# Remove background
print("\n5. Removing background...")
remove_bg = client.midjourney.remove_background(job_id=job_id, image_no=0)
remove_bg_result = client.tasks.wait_for_completion(remove_bg.job_id)
print(f"No background: {remove_bg_result.output.image_url}")
