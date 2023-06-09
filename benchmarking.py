""" Benchmarking functions and decorators. """
import pstats
import time
import cProfile


def profile_with_cprofile(func):
    """
    A decorator to profile a function.
    """
    def function_profiler(*args, **kwargs):
        with cProfile.Profile() as pr:
            value = func(*args, **kwargs)
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        return value

    return function_profiler


def time_function(func):
    """
    A decorator to time a function.
    """
    def function_timer(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        runtime = end - start
        print(f"The function {func.__name__} took {runtime} seconds.")
        return value

    return function_timer
