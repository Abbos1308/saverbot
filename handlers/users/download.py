import aiohttp
import asyncio

headers = {'Host': 'tikcdn.io', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': 'Windows', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'https://www.instagram.com/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5'}

async def download_file(url, filename):
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

