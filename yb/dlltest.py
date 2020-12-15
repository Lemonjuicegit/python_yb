import ctypes
import os
import pk.decoratorsFunc as decorators

dllpath = {"testdll": r"D:\program_c++\Dllpk\x64\Release"}


@decorators.runtime
def dll(path, dllfilename, funcname):
    dllpk = ctypes.cdll.LoadLibrary(os.path.join(dllpath[path], dllfilename))

    # return dllpk.dlltest.add(a,r)
    func = getattr(dllpk, funcname)
    return func(2, 6)


@decorators.getexceptionreturn
@decorators.runtimereturn
def d():
    a = 0
    for i in range(0, 1000):
        a += i
    return a


if __name__ == '__main__':
    # a = dll("testdll", "Dllpk.dll", "dlltest")
    g=d("sasf")
    print(g)
    # print("--------------")