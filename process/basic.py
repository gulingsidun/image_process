import tkinter as tk
from distutils.dist import command_re
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class BasicProcessing:
    def __init__(self, image):
        self.image = image

    def display_image_info(self,path):
        if self.image is None:
            messagebox.showwarning("警告", "没有可显示的图像信息")
            return

        # 获取图像基本信息
        height, width = self.image.shape[:2]
        channels = self.image.shape[2] if len(self.image.shape) > 2 else 1
        is_color = channels > 1
        dtype = self.image.dtype
        bit_depth = dtype.itemsize * 8
        file_size = self.image.nbytes

        # 创建信息字符串
        info = f"图像基本信息:\n"
        info += f"图片位置："+path+"\n"
        info += f"大小: {width} x {height} 像素\n"
        info += f"像素位置: (0, 0) 到 ({width}, {height})\n"
        info += f"分辨率: {width} x {height} 像素\n"
        info += f"通道数量: {channels}\n"
        info += f"类型: {'彩色图' if is_color else '灰度图'}\n"
        info += f"位深度: {bit_depth} 位\n"
        info += f"存储大小: {file_size} 字节"

        # 显示信息
        messagebox.showinfo("图像信息", info)

    def image_crop(self, x1, y1, x2, y2):
        if self.image is None:
            messagebox.showwarning("警告", "没有可操作的图像")
            return
        try:
            self.image = self.image[y1:y2, x1:x2]
            return self.image
        except Exception as e:
            messagebox.showerror("错误", f"裁剪失败: {str(e)}")

    def image_resize(self, width, height):
        if self.image is None:
            messagebox.showwarning("警告", "没有可操作的图像")
            return
        try:
            self.image = cv2.resize(self.image, (width, height))
            return self.image
        except Exception as e:
            messagebox.showerror("错误", f"调整尺寸失败: {str(e)}")

    def image_rotate(self, angle):
        if self.image is None:
            messagebox.showwarning("警告", "没有可操作的图像")
            return
        try:
            (h, w) = self.image.shape[:2]
            (cX, cY) = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
            self.image = cv2.warpAffine(self.image, M, (w, h))
            return self.image
        except Exception as e:
            messagebox.showerror("错误", f"旋转失败: {str(e)}")

    def get_processed_image(self):
        return self.image