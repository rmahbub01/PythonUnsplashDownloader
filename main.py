import asyncio
import time

from unsplashDownloader import Unsplash

loop = asyncio.get_event_loop()
unsplash = Unsplash('cat', 50, quality='raw', pages=2)
name_url = unsplash.downloadImg()

sem = asyncio.Semaphore(5)


async def finalDl(j, i):
    async with sem:
        return await unsplash.saveImg(j, i)


async def main():
    futures = [
        asyncio.ensure_future(finalDl(j, i)) for i, j in name_url.items()
    ]
    return await asyncio.gather(*futures)


start = time.time()
loop.run_until_complete(main())
stop = time.time()

print(f"total time: {round(stop-start, 1)}seconds")
