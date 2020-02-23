import time

MAX_COUNT = 100_000_000

def counter(n):
    for _ in range(n):
        pass

def buildTasks():
    start = time.perf_counter_ns()
    counter(MAX_COUNT)
    stop = time.perf_counter_ns()

    delta = (stop - start) / 1_000_000
    print(f"1 tasks launched | Total time : {delta:.2f} ms")

def main():
    buildTasks()

if __name__ == "__main__":
    main()