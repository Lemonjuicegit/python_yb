def share_area(share_area, area_list):
    """
    @param share_area: 共用面积列表
    @param area_list: 独用面积列表
    @return: 返回分摊面积列表
    """
    gross_area = 0
    for i in area_list:
        gross_area += i

    ratio = []  # 分摊系数
    for i in area_list:
        ratio.append(i / gross_area)
    ratio_area = []  # 分摊面积列表
    for i in share_area:
        tmpe = []
        for n in ratio:
            tmpe.append(round(i * n,2))
        ratio_area.append(tmpe)
    ratio_area.append([round(i,4) for i in ratio])
    ratio_area=[str(i) for i in ratio_area]

    ratio_area="\n".join(ratio_area)
    return ratio_area

if __name__ == '__main__':
    a="82.88 55.12 82.66"
    b=a.split(" ")
    b=[float(i) for i in b]
    print(b)
