import ctypes
import os
from pk import decoratorsFunc

dllpath = {"testdll": r"D:\program_c++\Dllpk\x64\Release"}


@decoratorsFunc.runtime
def dll(path, dllfilename, funcname):
    dllpk = ctypes.cdll.LoadLibrary(os.path.join(dllpath[path], dllfilename))

    # return dllpk.dlltest.add(a,r)
    func = getattr(dllpk, funcname)
    return func(2, 6)


@decoratorsFunc.runtime
def d():
    a=0
    for i in range(0, 100000001):
        a += i

    print(a)


if __name__ == '__main__':
    a = dll("testdll", "Dllpk.dll", "dlltest")
    d()
    print("--------------")
