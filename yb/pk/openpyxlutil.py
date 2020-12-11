from openpyxl import *

"""读取指定excel表一列的值，并回一个列表"""
def excel_field(path, string, sheet_name="Sheet1"):  # path:excel表路径, string：excel表列名（A,B,C....）,sheet:工作表名称

    field = []
    i = 2
    execl_gjb = load_workbook(path, data_only=True)
    sheets = execl_gjb[sheet_name]
    while sheets[string + str(i)].value != None:
        field.append(sheets[string + str(i)].value)
        i += 1
    return field
