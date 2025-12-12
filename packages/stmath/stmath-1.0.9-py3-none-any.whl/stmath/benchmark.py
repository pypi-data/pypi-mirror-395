# \"\"\"Simple micro-benchmark helpers\"\"\"
import time, tracemalloc


def timeit(fn, *args, runs=100, **kwargs):
    t0 = time.perf_counter()
    for _ in range(runs):
        fn(*args, **kwargs)
    t1 = time.perf_counter()
    return (t1 - t0) / runs


def mem_profile(fn, *args, **kwargs):
    tracemalloc.start()
    fn(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return current, peak
