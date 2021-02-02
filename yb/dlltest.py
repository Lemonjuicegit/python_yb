from ctypes import *
import os
import pk.decoratorsFunc as decorators
from multiprocessing import process

dllpath = {"testdll": r"D:\program_c++\Project1"}

# @decorators.runtime
def dll(path, dllfilename, funcname):
    """
    @param path:链接库的路径
    @param dllfilename:链接库的方法名
    @param funcname:要执行的方法名
    @return:
    """
    dllpk = cdll.LoadLibrary(os.path.join(path, dllfilename))
    # return dllpk.dlltest.add(a,r)
    func = getattr(dllpk, funcname)
    return func


def c_dll(path):
    dll = CDLL(path)
    return dll


@decorators.getexceptionreturn
@decorators.runtimereturn
def d():
    a = 0
    for i in range(0, 1000):
        a += i
    return a

if __name__ == '__main__':
    # a = dll(r"D:\program_c++\Project1", "tast.dll", "__cname")
    # g=a()
    # print(hex(g))

    dll = c_dll(r"D:\program_c++\Project1\lic.dll")
    a = dll.getlic()
    print(a)
