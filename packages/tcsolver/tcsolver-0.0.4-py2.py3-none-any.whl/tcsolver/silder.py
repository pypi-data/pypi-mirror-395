from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
import time
import random
import tcsolver.image_utility as imageutil


@dataclass
class SliderOptions:
    validateButtonSelector: str = "#captcha_click"
    iframeSelector: str = "#tcaptcha_iframe_dy"
    sliderBarSelector: str = "div.tc-slider-normal"

def get_track_list(distance):
    """
    模拟轨迹（位移序列）以拟人化拖拽：先加速后减速，并在终点附近产生轻微回退
    """
    v = 0  # 初速度
    t = 0.2  # 采样时间片，单位秒；每个轨迹点代表0.2s内的位移
    tracks = []  # 轨迹列表
    current = 0  # 当前累计位移
    mid = distance * 7 / 8  # 约在终点附近开始减速，防止“撞线”过头

    distance += 10  # 故意超过目标一点，稍后反向小幅回滑，更像人工操作
    # a = random.randint(1,3)
    while current < distance:
        if current < mid:
            # 前段加速：加速度较小能得到更细密的轨迹（更平滑）
            a = random.randint(2, 4)
        else:
            # 后段减速：负加速度
            a = -random.randint(3, 5)

        v0 = v  # 记录上一步的速度
        s = v0 * t + 0.5 * a * (t ** 2)  # 匀加速位移公式
        current += s  # 更新累计位移
        tracks.append(round(s))  # 记录本时间片的位移（取整像素）

        v = v0 + a * t  # 更新速度，作为下一时间片的初速度

    # 终点附近的小幅回退，模拟手部调整以对齐缺口
    for i in range(4):
        tracks.append(-random.randint(2, 3))
    for i in range(4):
        tracks.append(-random.randint(1, 3))
    return tracks


def dragbox_location(page, options: SliderOptions):
    # 多次尝试从验证码iframe中定位到拖动滑块的元素区域
    for i in range(5):
        dragbox_bounding = page.frame_locator(options.iframeSelector).locator(
            options.sliderBarSelector).bounding_box()
        # 当成功拿到坐标并且x位置合理（>20避免无效值）时返回位置信息
        if dragbox_bounding is not None and dragbox_bounding["x"] > 20:
            return dragbox_bounding
    # 若未定位到滑块，返回None以供上层处理
    return None

def drag_to_breach(page, move_distance, options: SliderOptions):
    # 根据预生成的轨迹（move_distance）模拟人手拖拽滑块
    print('开始拖动滑块..')
    drag_box = dragbox_location(page, options)
    if drag_box is None:
        print('未获取到滑块位置,识别失败')
        return False
    # 将鼠标移动到滑块中心位置并按下
    page.mouse.move(drag_box["x"] + drag_box["width"] / 2,
                    drag_box["y"] + drag_box["height"] / 2)
    page.mouse.down()
    location_x = drag_box["x"]  # 当前鼠标的x位置，从滑块起点开始
    # 按轨迹逐步移动，模拟有加减速的人为拖拽
    for i in move_distance:
        location_x += i
        page.mouse.move(location_x, drag_box["y"])
    # 松开鼠标，完成拖动
    page.mouse.up()
    # 通过页面文案简单判断是否通过或需要重试（此处仅为示例）
    if page.get_by_text("后重试") is not None or page.get_by_text("请控制拼图对齐缺口") is not None:
        print("识别成功")
        return True
    print('识别失败')
    return False

def solve_slider(page, options: SliderOptions):
    store = {"bg_image_name": None}

    def handle(route, request):
        try:
            response = route.fetch()
            if response.status == 200 and "index=1" in request.url:
                parsed_url = urlparse(request.url)
                bg_image_name = parse_qs(parsed_url.query).get("image", [""])[0]
                store["bg_image_name"] = f"{bg_image_name}.png"
                buffer = response.body()
                filename = f"{bg_image_name}.png"
                with open(filename, "wb") as f:
                    f.write(buffer)
        finally:
            route.continue_()

    page.route("**/turing.captcha.qcloud.com/cap_union_new_getcapbysig**", handle)

    # page.locator(options.validateButtonSelector).scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    page.locator(options.validateButtonSelector).first.click()

    frame = page.wait_for_selector(options.iframeSelector)
    print(frame.bounding_box())

    deadline = time.time() + 10
    while store["bg_image_name"] is None and time.time() < deadline:
        page.wait_for_timeout(100)

    bg_image_name = store["bg_image_name"]

    if bg_image_name:
        print("bg_image_name:" + bg_image_name)
    
    distance = imageutil.calc_gap_distance(bg_image_name)
    page.wait_for_timeout(200)
    print("distance:" + str(distance))

    relevant_distance = distance * 349 / 672
    move_distance = get_track_list(relevant_distance)
    print(f"获取到相对滑动距离{relevant_distance}, 模拟拖动列表{move_distance}")

    success = drag_to_breach(page, move_distance, options)


