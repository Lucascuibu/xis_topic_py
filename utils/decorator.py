import time


def async_timeit(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} costs {end_time - start_time:.5f} seconds")

        return result

    return wrapper

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} costs {end_time - start_time:.5f} seconds")

        return result

    return wrapper
