import ctypes
import os

dllpath = {"testdll": r"D:\program_c++\Dllpk\x64\Release"}


def dll(path, dllfilename, funcname, a,r):
    dllpk = ctypes.cdll.LoadLibrary(os.path.join(dllpath[path],dllfilename))
    func = getattr(dllpk, funcname)
    return func(a,r)


if __name__ == '__main__':
    a = dll("testdll", "Dllpk.dll", "add", 2, 5)
    print(a)
