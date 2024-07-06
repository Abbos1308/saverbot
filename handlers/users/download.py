import aiohttp
import asyncio


async def download_file(url, filename,headers=None):
    try:
        async with aiohttp.ClientSession() as session:
            
            async with session.get(url,headers=headers) as response:
                if response.status == 200:
                    data = await response.read()
                    with open(filename, "wb") as f:
                        f.write(data)
                    print(f"Downloaded {filename} successfully!")
                else:
                    print(f"Error: Status code {response.status} received.")
    except Exception as e:
        print(f"An error occurred: {e}")

