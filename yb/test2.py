from pk import fileutil
from pandas import DataFrame,read_excel

def exf(data_path,paper_path):
    file_path = fileutil.getfilepath(paper_path)
    exfdata = fileutil.read_exf(file_path)
    comparison_d = {"宗地代码": [], "权利人姓名": [], "宗地面积对比": [], "宗地代码是否重复": []}
    comparison = DataFrame(columns=["宗地代码", "权利人姓名", "宗地面积对比", "宗地代码是否重复"])  # 检查结果集
    for i in exfdata.itertuples():
        data = read_excel(data_path)
        zdmj_comparison = float(data[data["宗地代码"] == getattr(i, "宗地代码")]["宗地面积"]) == getattr(i, "宗地面积")
        comparison_d["宗地代码"].append(getattr(i, "宗地代码"))
        comparison_d["宗地面积对比"].append(zdmj_comparison)
        comparison_d["权利人姓名"].append(getattr(i, "权利人姓名"))
        comparison_temp = DataFrame(comparison_d)
        comparison.append(comparison_temp, ignore_index=True)

if __name__ == '__main__':
    print(execl_gjb["身份证"])