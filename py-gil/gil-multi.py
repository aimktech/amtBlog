import time
from multiprocessing import Process

MAX_COUNT = 100_000_000

def counter(n):
    for _ in range(n):
        pass

def buildTasks(n):
    tasks = []

    # create some threads
    for _ in range(n):
        tasks.append(
            Process(target=counter, args=(MAX_COUNT//n,))
        )
    
    start = time.perf_counter_ns()
    [ t.start() for t in tasks ]
    [ t.join() for t in tasks ] 
    stop = time.perf_counter_ns()

    delta = (stop - start) / 1_000_000
    print(f"{n:02d} tasks launched | Total time : {delta:.2f} ms")
    
def main():
    for i in range(10):
        buildTasks(i+1)

if __name__ == "__main__":
    main()
