import time
from concurrent.futures import ThreadPoolExecutor
import asyncio
from multiprocessing import Pool


def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    a = 0
    b = 1
    for i in range(1, n):
        c = a + b
        a = b
        b = c
    return b


async def fibonacci_async(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    a = 0
    b = 1
    for i in range(1, n):
        c = a + b
        a = b
        b = c
    return b


async def run_tasks_fibonacci_async(n: int, count: int):
    await asyncio.gather(*[fibonacci_async(n) for _ in range(count)])


def main():

    n = 500000
    tasks = 4
    print(f"n={n}")
    print(f"tasks={tasks}")

    start_time = time.time()
    fibonacci(n)
    print("synchronous=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    with ThreadPoolExecutor() as ex:
        for _ in range(tasks):
            ex.submit(fibonacci, n)
    print("multithreading=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks_fibonacci_async(n, tasks))
    print("asynchronous=", end="")
    print(time.time() - start_time)

    start_time = time.time()
    with Pool() as p:
        p.map(fibonacci, [n for _ in range(tasks)])
    print("multiprocessing=", end="")
    print(time.time() - start_time)


if __name__ == '__main__':
    main()