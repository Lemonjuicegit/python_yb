from time import time


def runtime(f):
    def run(*args, **kwargs):
        a = time()
        f(*args, **kwargs)
        d = time()
        print(d - a)

    return run

def runtimereturn(f):
    def run(*args, **kwargs):
        a = time()
        returnvalue = f(*args, **kwargs)
        d = time()
        print(d - a)
        return returnvalue

    return run

def getexception(f):
    def exception(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except BaseException as e:
            return str(e)

    return exception


def getexceptionreturn(f):
    def exception(*args, **kwargs):
        try:
            returnvalue = f(*args, **kwargs)
            return returnvalue
        except BaseException as e:
            return str(e)
        except AttributeError as e:
            return str(e)

    return exception
