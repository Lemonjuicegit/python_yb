from os import system,path

# 批量生成文件夹命令
class Cmd:

    #批量生成文件夹
    def paper_files(self,Dpath,name=[]):
        for i in name:
            system("md "+Dpath+"\\"+i)

    def isdir(self,Dpath):
        return path.isdir(Dpath)
