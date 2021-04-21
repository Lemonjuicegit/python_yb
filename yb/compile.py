#   这是一个批量生成.pyc
import py_compile
import os
def compile(path):

    a=os.path.split(path)
    for i in os.listdir(path):
        name=os.path.splitext(i)
        if name[1]==".py":
            print(path+"\\"+os.path.split(path)[1]+"\\"+name[0]+".pyc")
            py_compile.compile(os.path.join(path,i),path+"\\"+os.path.split(path)[1]+"\\"+name[0]+".pyc")

def intallpk():
    pass


if __name__ == '__main__':
    compile(r"D:\pythonProject\yb\pk")
    compile(r"D:\pythonProject\yb\WinUI")
    compile(r"D:\pythonProject\yb")

