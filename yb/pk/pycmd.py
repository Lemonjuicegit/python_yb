from os import system

# 批量生成文件夹命令
class Cmd:

    #批量生成文件夹
    def paper_files(self,path,name=[]):
        for i in name:
            system("md "+path+"\\"+i)