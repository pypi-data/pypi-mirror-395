"""Video generation example."""

import os

from legnext import Client

client = Client(api_key=os.environ.get("LEGNEXT_API_KEY"))

# Generate video with image URL in prompt
print("1. Generating video with image URL in prompt...")
response = client.midjourney.video_diffusion(
    prompt="https://example.com/your-image.jpg a serene mountain landscape with flowing clouds",
    video_type=1  # 720p quality
)
result = client.tasks.wait_for_completion(response.job_id, timeout=600)  # Videos take longer
print(f"Video URL: {result.output.image_url}")  # Video URL is in image_url field

# Extend the video
print("\n2. Extending video...")
extend = client.midjourney.extend_video(job_id=result.job_id)
extend_result = client.tasks.wait_for_completion(extend.job_id, timeout=600)
print(f"Extended video: {extend_result.output.image_url}")

# Upscale video
print("\n3. Upscaling video...")
upscale = client.midjourney.video_upscale(job_id=result.job_id)
upscale_result = client.tasks.wait_for_completion(upscale.job_id, timeout=600)
print(f"Upscaled video: {upscale_result.output.image_url}")
