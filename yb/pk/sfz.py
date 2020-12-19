# 这是一个处理身份证号码的class

class Sfz:

    def __init__(self, sfz_list=[]):
        self.checkcode = ("1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2")
        self.sfz_list = sfz_list

        def check_num(num):
            if len(num) == 18:
                num = int(num[0]) * 7 + int(num[1]) * 9 + int(num[2]) * 10 + int(num[3]) * 5 + int(
                    num[4]) * 8 + int(num[5]) * 4 + int(num[6]) * 2 + int(num[7]) * 1 + int(
                    num[8]) * 6 + int(num[9]) * 3 + int(num[10]) * 7 + int(num[11]) * 9 + int(
                    num[12]) * 10 + int(num[13]) * 5 + int(num[14]) * 8 + int(num[15]) * 4 + int(
                    num[16]) * 2
                checkvalue = num % 11
                return checkvalue
            else:
                checkvalue = "身份证号码位数错了！"
                return checkvalue

        self.checkvalue_list = []
        for i in sfz_list:
            self.checkvalue_list.append(check_num(i))

        self.checkvalue_list = tuple(self.checkvalue_list)  # 校验值元组

    def check_list(self):
        check_TF = []
        n = 0
        for i in self.checkvalue_list:
            if isinstance(i, int):
                if self.checkcode[i] != self.sfz_list[n][17]:
                    check_TF.append("第%s个 %s:身份证号码错了！\n" % (n + 1, self.sfz_list[n]))
            else:
                check_TF.append(r"第%s行 %s:%s\n" % (n + 1, self.sfz_list[n], self.checkvalue_list[n]))
            n += 1
        return check_TF

if __name__ == '__main__':
    a = "510224196511026333"

    sfz = Sfz(a)
    print(sfz.check())
    print(sfz.num)
