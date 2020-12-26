import cv2
import numpy as np


class Compress_img:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img_name = img_path.split('/')[-1]

    def compress_img_CV(self, compress_rate=0.5, show=False):
        img = cv2.imread(self.img_path)
        width = img.shape[:2]
        heigh = img.shape[:2]
        # 双三次插值
        img_resize = cv2.resize(img, (int(width[0] * compress_rate), int(heigh[1] * compress_rate)),
                                interpolation=cv2.INTER_AREA)
        cv2.imwrite('result_cv_' + self.img_name, img_resize)
        print("%s 已压缩，" % (self.img_name), "压缩率：", compress_rate)
        if show:
            cv2.imshow(self.img_name, img_resize)
            cv2.waitKey(0)


def main():
    # 1.随机创建图片
    img_src = cv2.imread(filename="qwer.jpg")
    print(img_src.shape[1])
    height, width = img_src.shape[:2]
    print("img width:%d height:%d" % (width, height))

    # 2.创建X,Y map
    map_x = np.zeros([width, height], np.float32)
    map_y = np.zeros([width, height], np.float32)

    # 3.执行重映射 调整 X Y map位置
    for i in range(width):
        for j in range(height):
            map_x.itemset((i, j), i)
            map_y.itemset((i, j), j)

    # 4.执行重映射处理
    cv2.remap(img_src, map_x, map_y, cv2.INTER_LINEAR)

    # 5.显示结果
    cv2.imwrite('result_cv_.jpg', img_src)
    cv2.imshow("img_src", img_src)
    cv2.imshow("img_dst", img_dst)

    cv2.waitKey()
    cv2.destroyAllWindows()

def a(d,c):
    print("sdfd---%s%s" % (d, c))

if __name__ == '__main__':

    main()
# img_path = r'./ym.jpg'
# compress = Compress_img(img_path)
#
# # 使用opencv压缩图片
# compress.compress_img_CV()
