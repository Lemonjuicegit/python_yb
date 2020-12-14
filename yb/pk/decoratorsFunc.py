import os
from time import time


def runtime(f):
    def run(*args, **kwargs):
        a = time()
        f(*args, **kwargs)
        d = time()
        print(d - a)
    return run


