from pandas import read_excel, DataFrame,concat
import os

def mergeForm(path,save_path):
    listpath=[]
    for i in os.listdir(path):
        if ".xlsx" in i:
            listpath.append(read_excel(os.path.join(path,i),dtype=str))
    df = concat(listpath)
    df.to_excel(save_path,index=False)

if __name__=="__main__":
    cun=["金刚村","良桥村","石坪村","五通庙村","新合村","新乡村","学堂村","垭口村"]
    for i in cun:

        excel=os.path.join(r"G:\成果提交\木耳镇\数据库及台账",i)
        save=os.path.join(r"G:\成果提交\木耳镇\数据库及台账",i,"渝北区木耳镇%s存量工作台账（总）.xlsx"%i)
        mergeForm(excel,save)



