import aiohttp
import asyncio

async def download_file(url, filename):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    with open(filename, "wb") as f:
                        f.write(data)
                    print(f"Downloaded {filename} successfully!")
                else:
                    print(f"Error: Status code {response.status} received.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
asyncio.run(download_file("https://tikcdn.io/ssstik/7357903815397428481", "22.mp4"))
