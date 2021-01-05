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
        ratio = []
        for n in ratio:
            ratio.append(round(i * n))
        ratio_area.append(ratio)
    return ratio_area


if __name__ == '__main__':
    a=[1,2,4]
    c=(b in a)