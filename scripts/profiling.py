from time import perf_counter


def profile_decorator(func):
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        result = func(*args, **kwargs)
        t1 = perf_counter()
        with open("threshold.txt","a") as file:
            file.write(str(t1-t0)+'\n')
        return result
    return wrapper
    
