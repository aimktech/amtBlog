import time
import asyncio

MAX_COUNT = 100_000_000

async def counter(n):
    for _ in range(n):
        pass

async def buildTasks(n):
    tasks = []

    # create some threads
    for _ in range(n):
        tasks.append(
            asyncio.create_task(counter(MAX_COUNT//n))
        )
    
    start = time.perf_counter_ns()
    await asyncio.gather(*tasks)
    stop = time.perf_counter_ns()

    delta = (stop - start) / 1_000_000
    print(f"{n:02d} threads launched | Total time : {delta:.2f} ms")
    
async def main():
    for i in range(10):
        await buildTasks(i+1)

if __name__ == "__main__":
    asyncio.run(main())
