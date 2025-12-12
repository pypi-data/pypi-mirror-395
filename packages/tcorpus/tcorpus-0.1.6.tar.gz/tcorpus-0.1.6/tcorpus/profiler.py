from datetime import datetime
import threading


def timed(func):
    """Time function execution using datetime."""
    def wrapper(*args, **kwargs):
        start = datetime.now()
        out = func(*args, **kwargs)
        end = datetime.now()
        elapsed = (end - start).total_seconds()
        return out, elapsed
    return wrapper


def threaded(target, *args):
    t = threading.Thread(target=target, args=args)
    t.start()
    t.join()
