import time
from concurrent.futures import ThreadPoolExecutor
import asyncio
from multiprocessing import Pool
import aiohttp
import requests
import bs4


headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
}
search_title = False


def make_request_and_get_title(url: str):
    resp = requests.get(url=url, headers=headers)
    if resp.status_code != 200:
        return False
    if search_title:
        soup = bs4._soup(resp.text, "html.parser")
        title = soup.find("span", {"class": "mw-page-title-main"})
        if title is None:
            return False
        return title.text


async def make_request_and_get_title_async(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            if resp.status != 200:
                return False
            page = await resp.text()
            if search_title:
                soup = bs4._soup(page, "html.parser")
                title = soup.find("span", {"class": "mw-page-title-main"})
                if title is None:
                    return False
                return title.text


async def run_tasks(urls: list):
    await asyncio.gather(*[make_request_and_get_title_async(url) for url in urls])


def run(tasks, url):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks([url for _ in range(int(tasks/4))]))


def main():

    url = "https://uk.m.wikipedia.org/wiki/%D0%97%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D0%B9_%D0%BD%D0%B5%D1%80%D0%B2"
    tasks = 40
    print(f"tasks={tasks}")

    start_time = time.time()
    make_request_and_get_title(url)
    print("synchronous=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    with ThreadPoolExecutor() as ex:
        for _ in range(tasks):
            ex.submit(make_request_and_get_title, url)
    print("multithreading=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks([url for _ in range(tasks)]))
    print("asynchronous=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    with Pool() as p:
        p.map(make_request_and_get_title, [url for _ in range(tasks)])
    print("multiprocessing=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    with Pool() as p:
        p.starmap(run, [(tasks, url) for _ in range(4)])
    print("multiprocessing + asynchronous=", end="")
    print(time.time() - start_time)


if __name__ == '__main__':
    main()