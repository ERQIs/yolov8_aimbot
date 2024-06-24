
import pygetwindow as gw
import mss
import numpy as np
import cv2

class windowGrabber:
    def __init__(self, windowName: str, picture_size = (640, 640)) -> None:
        try:
            self.sct = mss.mss()
            self.picture_size = picture_size
            windows = gw.getWindowsWithTitle(windowName)
            self.window = windows[0]
            self.monitor = {"top": self.window.top, "left": self.window.left, "width": self.window.width, "height": self.window.height}
        except BaseException as e:
            print(e)
            raise(Exception("faild to initialize windowGrabber"))

    def grab(self):
        """
            返回一个cv2使用的格式的窗口截图
        """
        # 更新 monitor

        self.monitor["top"] = self.window.top
        self.monitor["left"] = self.window.left
        self.monitor["width"] = self.window.width
        self.monitor["height"] = self.window.height
        # 截图
        screenshot = self.sct.grab(self.monitor)
        # 将截图转换为NumPy数组
        img = np.array(screenshot)
        # 将图像从BGRA转换为BGR（OpenCV使用BGR格式）
        img = img[..., :3]
        img_resized = cv2.resize(img, self.picture_size)
        return img_resized

    def grab_in_window(self, width: int, height: int):
        """
            返回一个cv2使用的格式的窗口截图
            截取窗口中央长度为width， 高度为height的图像区域
        """
        # 更新 monitor
        t = self.window.top
        l = self.window.left
        w = self.window.width
        h = self.window.height

        # 重新划定截图区域
        mid_y = t + h//2
        mid_x = l + w//2
        new_t = mid_y - height//2
        new_l = mid_x - width//2
        if new_t > t:
            t = new_t
            h = height
        if new_l > l:
            l = new_l
            w = width

        # 写回到 monitor
        self.monitor["top"] = t
        self.monitor["left"] = l
        self.monitor["width"] = w
        self.monitor["height"] = h

        # 截图
        screenshot = self.sct.grab(self.monitor)
        # 将截图转换为NumPy数组
        img = np.array(screenshot)
        # 将图像从BGRA转换为BGR（OpenCV使用BGR格式）
        img = img[..., :3]
        img_resized = cv2.resize(img, self.picture_size)
        return img_resized