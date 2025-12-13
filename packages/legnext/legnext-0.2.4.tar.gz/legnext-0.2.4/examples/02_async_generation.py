"""Async image generation example."""

import asyncio
import os

from legnext import AsyncClient


async def main():
    # Initialize the async client
    async with AsyncClient(api_key=os.environ.get("LEGNEXT_API_KEY")) as client:
        # Generate an image
        print("Generating image...")
        response = await client.midjourney.diffusion(text="a futuristic cityscape at night")

        print(f"Job ID: {response.job_id}")
        print(f"Status: {response.status}")

        # Wait for completion
        print("\nWaiting for completion...")
        result = await client.tasks.wait_for_completion(response.job_id)

        # Print results
        print("\nCompleted!")
        print(f"Generated {len(result.output.image_urls)} images:")
        for i, url in enumerate(result.output.image_urls, 1):
            print(f"  Image {i}: {url}")


if __name__ == "__main__":
    asyncio.run(main())
