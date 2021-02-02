#   这是一个批量生成.pyc的class
import py_compile
import os

filepath=input("输入源文件路径:")
a=os.path.split(filepath)
for i in os.listdir(filepath):
    name=os.path.splitext(i)
    if name[1]==".py":
        print(filepath+name[0]+".pyc")
        py_compile.compile(os.path.join(filepath,i),filepath+"\\"+os.path.split(filepath)[1]+"\\"+name[0]+".pyc")


