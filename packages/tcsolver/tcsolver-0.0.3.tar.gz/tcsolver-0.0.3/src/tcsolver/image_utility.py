import cv2
import numpy as np
import pandas as pd
import math


# x方向一阶导中值
# 提取在矩形区域内，沿x方向的一阶Sobel梯度的中位数，度量横向边缘强度
def get_dx_median(dx, x, y, w, h):
    return np.median(dx[y:(y + h), x])

# 预处理：读图、灰度化、二值化与轮廓提取
def pre_process(img_path):
    print("pre_process.img_path" + img_path)
    img = cv2.imread(img_path, 1)  # 读取原始BGR图像
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成灰度图像，降低通道维度方便阈值化
    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)  # 全局阈值二值化，提取前景/背景
    contours, _hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 查找所有轮廓

    rect_area = []  # 记录候选矩形面积
    rect_arc_length = []  # 记录候选矩形周长
    cnt_infos = {}  # 存放候选轮廓及衍生特征

    for i, cnt in enumerate(contours):
        # 依据面积粗筛缺口候选的轮廓，过滤过小/过大的区域
        if cv2.contourArea(cnt) < 5000 or cv2.contourArea(cnt) > 25000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)  # 获取轮廓外接矩形
        cnt_infos[i] = {'rect_area': w * h,  # 矩形面积
                        'rect_arclength': 2 * (w + h),  # 矩形周长
                        'cnt_area': cv2.contourArea(cnt),  # 原始轮廓面积
                        'cnt_arclength': cv2.arcLength(cnt, True),  # 原始轮廓周长
                        'cnt': cnt,  # 轮廓对象
                        'w': w,
                        'h': h,
                        'x': x,
                        'y': y,
                        # 取矩形内像素的最小值（各通道最小）后求平均，刻画区域亮/暗程度
                        'mean': np.mean(np.min(img[y:(y + h), x:(x + w)], axis=2)),
                        }
        rect_area.append(w * h)
        rect_arc_length.append(2 * (w + h))
    # 计算Sobel x方向梯度，用于衡量垂直边缘强度
    dx = cv2.Sobel(img, -1, 1, 0, ksize=5)
    return img, dx, cnt_infos


def get_mark_pos(img_path):
    img, dx, cnt_infos = pre_process(img_path)
    # 将轮廓特征字典转为DataFrame，便于“特征工程+筛选排序”
    df = pd.DataFrame(cnt_infos).T
    df.head()
    # 计算每个候选区域的x方向梯度中值
    df['dx_mean'] = df.apply(lambda x: get_dx_median(dx, x['x'], x['y'], x['w'], x['h']), axis=1)
    # 计算矩形周长与面积的比值的“规范化”，接近1的更趋近于规则矩形
    df['rect_ratio'] = df.apply(lambda v: v['rect_arclength'] / 4 / math.sqrt(v['rect_area'] + 1), axis=1)
    # 计算矩形面积与轮廓面积的比值，越接近1说明轮廓与矩形贴合较好
    df['area_ratio'] = df.apply(lambda v: v['rect_area'] / v['cnt_area'], axis=1)
    # 偏离1的程度作为得分，越小越好（更规则）
    df['score'] = df.apply(lambda x: abs(x['rect_ratio'] - 1), axis=1)

    # 一系列条件过滤后，按亮度均值、规则度评分、边缘强度排序，取前2个作为候选
    result = df.query('x>0').query('area_ratio<2').query('rect_area>5000').query('rect_area<20000').sort_values(
        ['mean', 'score', 'dx_mean']).head(2)
    return result



def calc_gap_distance(bg_image_name: str):
    res = get_mark_pos(bg_image_name)  # 返回一个DataFrame，包含候选缺口的特征与x坐标
    return res.x.values[0]  # 取第一候选的x坐标作为缺口位置

