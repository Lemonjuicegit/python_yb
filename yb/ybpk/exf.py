from pk import fileutil
from os import path

def read_exf(path):
    exf=open(path)
    exf_sring=list(exf)
    for i in exf_sring:
        print(i)




    exf.close()


if __name__ == '__main__':
    path=r"D:\pythonProject\500112002021JC00001曹敏上传.exf"
    read_exf(path)