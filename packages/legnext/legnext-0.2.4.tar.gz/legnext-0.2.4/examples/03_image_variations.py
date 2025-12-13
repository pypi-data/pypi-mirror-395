"""Image variation and upscaling example."""

import os

from legnext import Client

client = Client(api_key=os.environ.get("LEGNEXT_API_KEY"))

# Generate initial images
print("1. Generating initial images...")
response = client.midjourney.diffusion(text="a cute robot, cartoon style")
result = client.tasks.wait_for_completion(response.job_id)
print(f"Generated images: {result.job_id}")

# Create a variation of the first image (subtle)
print("\n2. Creating subtle variation of image 0...")
variation = client.midjourney.variation(
    job_id=result.job_id, image_no=0, type=0  # 0 = subtle variation
)
variation_result = client.tasks.wait_for_completion(variation.job_id)
print(f"Variation: {variation_result.output.image_url}")

# Upscale the second image
print("\n3. Upscaling image 1...")
upscale = client.midjourney.upscale(
    job_id=result.job_id, image_no=1, type=1  # 1 = creative upscale
)
upscale_result = client.tasks.wait_for_completion(upscale.job_id)
print(f"Upscaled: {upscale_result.output.image_url}")

# Reroll to get completely new images with same prompt
print("\n4. Rerolling to get new variations (🎲 button)...")
reroll = client.midjourney.reroll(job_id=result.job_id)
reroll_result = client.tasks.wait_for_completion(reroll.job_id)
print(f"New variations: {len(reroll_result.output.image_urls)} images")
