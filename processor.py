# -*- coding = utf-8 -*-
# @Time : 2024/6/23
# @Author : erqi
# @File : processor.py

"""
aimbot视觉处理模块，负责调用各种模型将图片转换为目标集合
"""
from ultralytics import YOLO

class yolov8Processor:
    """
    yolov8 pytorch模型
    """
    def __init__(self, model_path: str) -> None:
        try:
            self.model_path = model_path
            self.model = YOLO(model_path)
        except BaseException as e:
            print(e)
            raise("faild to initialize yolov8 processer")
    
    def process(self, picture, visualize: bool = False):
        results = self.model(picture)
        result = results[0]
        if visualize == True:
            return result.boxes, result.plot()
        else:
            return result.boxes, None
