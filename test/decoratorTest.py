import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result

    return wrapper

@timer_decorator
def slow_function():
    time.sleep(2)
    print("Slow function finished executing.")

@timer_decorator
def fast_function():
    time.sleep(0.5)
    print("Fast function finished executing.")

if __name__ == "__main__":
    slow_function()
    fast_function()
