from pandas import read_excel, DataFrame,concat
import os

def mergeForm(path,save_path):
    listpath=[]
    for i in os.listdir(path):
        listpath.append(read_excel(os.path.join(path,i)))
    df = concat(listpath)
    df.to_excel(save_path,index=False)

if __name__=="__main__":
    mergeForm(r"E:\工作文件\temp\0419木耳合并\新建文件夹",r"E:\工作文件\temp\0419木耳合并\新建文件夹\木耳镇总台账.xlsx")



