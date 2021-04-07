import os
from os import system, path


# 批量生成文件夹命令
class Cmd:

    # 批量生成文件夹
    def md(self, Dpath, name):
        system("md " + Dpath + "\\" + name)

    def copy(self, Y_path, copy_path):
        system("copy " + Y_path + " " + copy_path)

    def isdir(self, Dpath):
        return path.isdir(Dpath)


if __name__ == '__main__':
    a=Cmd()
    a.md(r"E:\工作文件\aaaaa","sadsa")

