import time
from functools import wraps


def retry(max_retries=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        raise Exception(f"Max retries {max_retries} exceeded") from e
                    time.sleep(delay)
            return None

        return wrapper

    return decorator
