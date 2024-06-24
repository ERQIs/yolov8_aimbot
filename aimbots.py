# -*- coding = utf-8 -*-
# @Time : 2024/6/23
# @Author : erqi
# @File : aimbotutils.py

import cv2
from math import dist
import time
from mouse import moveRel, leftClick, keyPress
from windowgrab import windowGrabber
from processor import yolov8Processor
import random as rd
import win32gui

class testinglotAimbot:
    """
    一个专门用来在CSGO创意工坊打t的机器人
    """
    class mode:
        aim = 1
        normal = 2

    def __init__(
            self, 
            window_name: str, 
            model_path: str, 
            visulize: bool = False,
            window_grabber_output_size: tuple = (640, 640), 
            cross: list = [320, 340],
            aim_cross: list = [320, 363],
            scaller: float = 0.8,
            aim_scaller: float = 0.4,
            activeness: int = 500,
            activeness_factor: int = 10, 
            activeness_trigger: int = 7,
            click_delay: int = 20
            ):
        self.windowName = window_name
        self.wg = windowGrabber(windowName=window_name, picture_size=window_grabber_output_size)
        self.processor = yolov8Processor(model_path=model_path)
        self.cross = cross
        self.aim_cross = aim_cross
        self.scaller = scaller
        self.aim_scaller = aim_scaller
        self.visulize = visulize
        self.aimMode = self.mode.normal
        self.activeness = activeness
        self.activeness_full = activeness
        self.activeness_factor = activeness_factor
        self.activeness_trigger = activeness_trigger
        self.click_delay = click_delay
        pass
    
    def break_mood(self, messy: int = 500):
        """
        让机器人从死循环中自救
        """
        view_direc = rd.randint(-1, 1)

        view_move = view_direc * ((messy // 2) + rd.randint(0, messy//2))
        moveRel(view_move, 0)
        keyPress('W', rd.uniform(messy/500, messy/200))


    def action(self, boxes):
        """
        机器人的决策函数
        """

        # 选取距离准心最近的目标
        target = None
        target_min = 99999
        target_size = None
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            target_mid = ((x1+x2)/2, (y1+y2)/2)
            dis = dist(self.cross, target_mid)
            if dis < target_min:
                target_min, target, target_size = dis, target_mid, (y2 - y1) * (x2 - x1)

        mouse_move = self.activeness_trigger
        if target != None:
            # 找到了一个目标
            if self.aimMode == self.mode.normal:
                # aimbot处于普通模式
                x_offset = int(self.scaller * int(target[0] - self.cross[0]))
                y_offset = int(self.scaller * int(target[1] - self.cross[1]))
                mouse_move = dist((x_offset, y_offset), (0, 0))
                if mouse_move > 5:
                    # 在普通模式下找到了目标，如果目标还没有与准星重叠，则移动鼠标接近目标
                    print("action 1")
                    moveRel(x_offset, y_offset)
                else:
                    # 目标距离准心已经和准星重叠，开火
                    print("action 2")
                    leftClick(self.click_delay)
                # 如果找到的目标的面积较小，则将aimbot转换为瞄准模式
                if self.aimMode == self.mode.normal and target_size < 200:
                    self.aimMode = self.mode.aim

            else:
                # 找到目标时aimbot处于瞄准模式
                x_offset = int(self.aim_scaller * (target[0] - self.aim_cross[0]))
                y_offset = int(self.aim_scaller * (target[1] - self.aim_cross[1]))
                mouse_move = dist((x_offset, y_offset), (0, 0))
                if mouse_move > 8:
                    # 目标还未与准心重叠则移动屏幕
                    print("action 3")
                    moveRel(x_offset, y_offset)
                else:
                    # 目标已经与准心重叠则开火
                    print("action 4")
                    leftClick(self.click_delay)
            

        elif self.aimMode == self.mode.aim:
            # 屏幕中未找到目标且处于瞄准模式则切换到普通模式
            self.aimMode = self.mode.normal
        else:
            # 屏幕中未找到目标且处于普通模式则移动并切换视角
            mouse_move = 500
            self.break_mood()
            self.activeness = self.activeness_full



        # 计算最近几次的平均鼠标移动距离，如果太小则说明系统可能陷入了死循环
        self.activeness = (self.activeness * (self.activeness_factor - 1) + mouse_move) // self.activeness_factor
        if self.activeness <= self.activeness_trigger:
            # gui.moveRel(xOffset=500 ,yOffset=0,duration=0,relative=True)
            self.break_mood()
            self.activeness = self.activeness_full
                

    def run(self):
        """
        机器人运行的主循环
        """
        
        while True:

            # 当游戏窗口不是活动窗口时暂停aimbot
            active_window = win32gui.GetForegroundWindow()
            if active_window == 0:
                time.sleep(1)
                continue
            elif win32gui.GetWindowText(active_window) != self.windowName:
                time.sleep(1)
                continue

            start_time = time.time()

            # 根据aimbot的模式确定是要截屏整个屏幕还是屏幕中央的瞄准区域
            if self.aimMode == self.mode.normal:
                window_pic = self.wg.grab()
            else:
                window_pic = self.wg.grab_in_window(512, 350)
            
            # 追踪截屏时间
            # end_time = time.time()
            # print("window grab: {:.2f}ms".format(end_time - start_time))

            # 使用process模块处理截屏图片
            boxes, img = self.processor.process(window_pic, visualize = True)

            # 机器人决策
            action_start_time = time.time()
            self.action(boxes)
            action_end_time = time.time()
            print("action: {:.2f}ms".format(action_end_time - action_start_time))


            # 追踪一次循环时间
            end_time = time.time()
            print("proccess: {:.2f}ms".format(end_time - start_time))

            # 如果设置为visualize模式则显示中间处理结果
            if self.visulize:
                cv2.imshow("YOLOv8 Detection on CS:GO", cv2.resize(img, (1024, 512)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


    def corss_align(self):
        """
        用于校准准心位置
        会在普通模式和瞄准模式下分别在进行，通过wasd控制绿色圆圈与准心重叠然后按下回车键即可
        """

        # 校准瞄准模式下的准心
        while True:
            window_pic = self.wg.grab_in_window(512, 350)
            pic = cv2.circle(img=window_pic, center=self.aim_cross, radius=3, color=(0, 256, 0))
            cv2.imshow("YOLOv8 Detection on CS:GO", cv2.resize(pic, (1024, 512)))
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 13:
                break
            elif key == ord('w'):
                self.aim_cross[1] -= 1
            elif key == ord('s'):
                self.aim_cross[1] += 1
            elif key == ord('a'):
                self.aim_cross[0] -= 1
            elif key == ord('d'):
                self.aim_cross[0] += 1
            print(self.aim_cross)

        # 校准普通模式下的准心
        while True:
            window_pic = self.wg.grab()
            pic = cv2.circle(img=window_pic, center=self.cross, radius=3, color=(0, 256, 0))
            cv2.imshow("YOLOv8 Detection on CS:GO", cv2.resize(pic, (1024, 512)))
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 13:
                break
            elif key == ord('w'):
                self.cross[1] -= 1
            elif key == ord('s'):
                self.cross[1] += 1
            elif key == ord('a'):
                self.cross[0] -= 1
            elif key == ord('d'):
                self.cross[0] += 1
            print(self.cross)
        cv2.destroyAllWindows()