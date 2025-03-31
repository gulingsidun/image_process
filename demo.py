import tkinter as tk
from distutils.dist import command_re
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# 导入 process 文件夹下的模块
import process
from page.ParameterFrame import ParameterFrame  # 导入 ParameterFrame 类

# 帮助功能
def show_about():
    messagebox.showinfo("关于", "数字图像处理软件\n版本 1.0\n基于 Python、Tkinter 和 OpenCV 等库开发\n感谢这些库的开源支持")


class MainPage:
    def __init__(self, root):

        self.root = root

        # 初始化变量
        self.original_image = None
        self.original_image_path = None
        self.processing_image = None
        self.saving_image = None
        self.parameter_frame = None
        self.original_label = None
        self.processed_label = None
        # 创建菜单栏
        self.create_menu()
        # 创建工具栏
        self.create_toolbar()
        # 创建图像显示区域
        self.create_display_area()
        # 创建参数框
        self.create_parameter_frame()
        # 初始化参数框
        self.initialize_parameter_frame()


    def create_menu(self):# 创建菜单栏
        menubar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="打开", command=self.open_image)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 图像处理菜单
        process_menu = tk.Menu(menubar, tearoff=0)

        # 基础操作子菜单
        basic_menu = tk.Menu(process_menu, tearoff=0)

        basic_menu.add_command(label="显示图像基本信息", command=self.display_basic_information_of_image)

        geometric_transformation_menu = tk.Menu(basic_menu, tearoff=0)
        geometric_transformation_menu.add_command(label="图像裁剪", command=self.image_crop)
        geometric_transformation_menu.add_command(label="尺寸调整", command=self.image_resize)
        geometric_transformation_menu.add_command(label="图像旋转", command=self.image_rotate)
        basic_menu.add_cascade(label="几何变换", menu=geometric_transformation_menu)

        tone_transformation_menu = tk.Menu(basic_menu, tearoff=0)
        tone_transformation_menu.add_command(label="色调调整", command=self.adjust_tone)
        tone_transformation_menu.add_command(label="饱和度调整", command=self.adjust_saturation)
        tone_transformation_menu.add_command(label="对比度调整", command=self.adjust_contrast)
        tone_transformation_menu.add_command(label="亮度调整", command=self.adjust_brightness)
        basic_menu.add_cascade(label="色调变换", menu=tone_transformation_menu)

        process_menu.add_cascade(label="基础操作", menu=basic_menu)

        # 图像增强子菜单
        enhance_menu = tk.Menu(process_menu, tearoff=0)

        histogram_menu = tk.Menu(enhance_menu, tearoff=0)
        histogram_menu.add_command(label="直方图展示", command=self.histogram_display)
        histogram_menu.add_command(label="直方图均衡化", command=self.histogram_equalization)
        histogram_menu.add_command(label="直方图规定化", command=self.histogram_specification)
        enhance_menu.add_cascade(label="直方图", menu=histogram_menu)

        smoothing_denoising_menu = tk.Menu(enhance_menu, tearoff=0)
        smoothing_denoising_menu.add_command(label="均值滤波", command=self.mean_filter)
        smoothing_denoising_menu.add_command(label="中值滤波", command=self.median_filter)
        smoothing_denoising_menu.add_command(label="最大值滤波", command=self.max_filter)
        smoothing_denoising_menu.add_command(label="最小值滤波", command=self.min_filter)
        smoothing_denoising_menu.add_command(label="高斯滤波", command=self.gaussian_filter)
        smoothing_denoising_menu.add_command(label="自适应滤波", command=self.adaptive_filter)
        enhance_menu.add_cascade(label="滤波去噪", menu=smoothing_denoising_menu)

        image_sharpening_menu = tk.Menu(enhance_menu, tearoff=0)
        image_sharpening_menu.add_command(label="unsharp锐化", command=self.unsharp_masking)
        image_sharpening_menu.add_command(label="Sobel算子锐化", command=self.sobel_sharpening)
        image_sharpening_menu.add_command(label="Roberts交叉算子锐化", command=self.roberts_sharpening)
        image_sharpening_menu.add_command(label="拉普拉斯滤波锐化", command=self.laplacian_sharpening)
        enhance_menu.add_cascade(label="图像锐化", menu=image_sharpening_menu)

        process_menu.add_cascade(label="图像增强", menu=enhance_menu)

        # 图像分析与转换子菜单
        analysis_and_transformation_menu = tk.Menu(process_menu, tearoff=0)

        analysis_and_transformation_menu.add_command(label="傅里叶变换", command=self.Fourier_transformation)

        color_space_conversion_menu = tk.Menu(analysis_and_transformation_menu, tearoff=0)
        color_space_conversion_menu.add_command(label="HSI空间", command=self.HSI_conversion)
        color_space_conversion_menu.add_command(label="HSV空间", command=self.HSV_conversion)
        analysis_and_transformation_menu.add_cascade(label="色彩空间转换", menu=color_space_conversion_menu)

        analysis_and_transformation_menu.add_command(label="灰度图转彩色图", command=self.Gray_image_to_color_image)

        process_menu.add_cascade(label="图像分析与转换", menu=analysis_and_transformation_menu)

        #图像AI处理子菜单
        AI_processing_menu = tk.Menu(process_menu, tearoff=0)

        AI_processing_menu.add_command(label="图像分割", command=self.image_segmentation)
        AI_processing_menu.add_command(label="边缘检测", command=self.edge_detection)
        AI_processing_menu.add_command(label="目标检测", command=self.object_detection)

        target_recognition_menu = tk.Menu(AI_processing_menu, tearoff=0)
        target_recognition_menu.add_command(label="动物识别", command=self.animal_recognition)
        target_recognition_menu.add_command(label="植物识别", command=self.plant_recognition)
        target_recognition_menu.add_command(label="昆虫识别", command=self.insect_recognition)
        AI_processing_menu.add_cascade(label="目标识别", menu=target_recognition_menu)

        process_menu.add_cascade(label="AI处理", menu=AI_processing_menu)

        # 日常图像处理
        daily_image_processing_menu = tk.Menu(process_menu, tearoff=0)
        daily_image_processing_menu.add_command(label="证件照换背景", command=self.id_photo_background_change)
        daily_image_processing_menu.add_command(label="图像超分", command=self.image_super_resolution)
        daily_image_processing_menu.add_command(label="图像压缩", command=self.image_compression)
        process_menu.add_cascade(label="日常图像处理", menu=daily_image_processing_menu)

        menubar.add_cascade(label="处理", menu=process_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)

    def create_toolbar(self):  # 创建工具栏
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)

        # 添加工具栏按钮
        open_btn = tk.Button(toolbar, text="打开", command=self.open_image)
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)

        save_btn = tk.Button(toolbar, text="保存", command=self.save_image)
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_display_area(self):
        # 创建一个外边框框架，增加与窗口边界的距离
        outer_frame = tk.Frame(self.root, bg="blue")
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建显示区域框架，并添加内边距
        display_frame = tk.Frame(outer_frame, bg="blue")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 原始图像显示区域
        self.original_label = tk.Label(display_frame, text="原始图像", bg="#f0f0f0")
        self.original_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 处理后图像显示区域
        self.processed_label = tk.Label(display_frame, text="处理后图像", bg="#f0f0f0")
        self.processed_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_parameter_frame(self):
        # 创建参数框
        self.parameter_frame = ParameterFrame(self.root)
        # 将参数框放置在图像显示区域下方
        self.parameter_frame.frame.pack(fill=tk.X, padx=10, pady=5, after=self.original_label.winfo_parent())

    def initialize_parameter_frame(self):
        # 初始化参数框，创建一个默认的参数输入框
        default_params = {
            "example_param": {"label": "示例参数", "type": "entry", "default": ""}
        }
        self.parameter_frame.set_params(default_params)

    # 文件操作
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("图像文件", "*.jpg;*.png;*.bmp;*.gif")])
        if file_path:
            # 检查文件是否存在
            import os
            if os.path.exists(file_path):
                self.original_image_path=file_path
                self.original_image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
                if self.original_image is None:
                    messagebox.showerror("错误", f"无法读取图像文件: {file_path}")
                else:
                    self.processing_image = self.original_image
                    self.display_original_image()
                    self.display_processing_image()
            else:
                messagebox.showerror("错误", f"文件不存在: {file_path}")

    def save_image(self):
        if self.processing_image is not None:
            self.saving_image = self.processing_image
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("BMP", "*.bmp"),
                    ("GIF", "*.gif")
                ]
            )
            if file_path:
                # 使用 cv2.imencode 将图像编码为字节数组
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                    img_encode = cv2.imencode('.jpg', self.saving_image, encode_param)[1]
                elif file_path.lower().endswith('.png'):
                    encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
                    img_encode = cv2.imencode('.png', self.saving_image, encode_param)[1]
                elif file_path.lower().endswith('.bmp'):
                    img_encode = cv2.imencode('.bmp', self.saving_image)[1]
                elif file_path.lower().endswith('.gif'):
                    img_encode = cv2.imencode('.gif', self.saving_image)[1]
                else:
                    messagebox.showerror("错误", "不支持的文件格式")
                    return

                # 将字节数组写入文件
                with open(file_path, 'wb') as f:
                    f.write(img_encode.tobytes())

                messagebox.showinfo("保存成功", f"图像已保存到: {file_path}")
        else:
            messagebox.showwarning("警告", "没有可保存的图像")

    # 图像显示
    def display_original_image(self):
        if self.original_image is not None:
            original_imgtk = self.convert_cv_to_tk(self.original_image)
            self.original_label.config(image=original_imgtk)
            self.original_label.image = original_imgtk

    def display_processing_image(self):
        if self.processing_image is not None:
            processed_imgtk = self.convert_cv_to_tk(self.processing_image)
            self.processed_label.config(image=processed_imgtk)
            self.processed_label.image = processed_imgtk

    def convert_cv_to_tk(self, cv_image):  # 将 OpenCV 格式的图像转换为 Tkinter 可以显示的格式
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(cv_image)

        # 获取显示区域的大小
        display_width = self.original_label.winfo_width()
        display_height = self.original_label.winfo_height()

        if display_width > 1 and display_height > 1:   # 确保显示区域已经被正确初始化
            # 计算缩放比例
            img_width, img_height = img.size
            width_ratio = display_width / img_width
            height_ratio = display_height / img_height
            scale_ratio = min(width_ratio, height_ratio)

        # 计算新的尺寸
            new_width = int(img_width * scale_ratio)
            new_height = int(img_height * scale_ratio)

        # 对图像进行缩放
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk



    #图像处理的功能实现函数
    # 图像基本信息
    def display_basic_information_of_image(self):
        new_window=process.basic.BasicProcessing(self.original_image)
        new_window.display_image_info(self.original_image_path)
    # 几何变换
    def image_crop(self):
        pass

    def image_resize(self):
        pass

    def image_rotate(self):
        pass

    # 色调变换
    def adjust_tone(self):
        pass

    def adjust_saturation(self):
        pass

    def adjust_contrast(self):
        pass

    def adjust_brightness(self):
        pass

    # 直方图
    def histogram_display(self):
        pass

    def histogram_equalization(self):
        pass

    def histogram_specification(self):
        pass

    # 滤波去噪
    def mean_filter(self):
        pass

    def median_filter(self):
        pass

    def max_filter(self):
        pass

    def min_filter(self):
        pass

    def gaussian_filter(self):
        pass

    def adaptive_filter(self):
        pass

    # 图像锐化
    def unsharp_masking(self):
        pass

    def sobel_sharpening(self):
        pass

    def roberts_sharpening(self):
        pass

    def laplacian_sharpening(self):
        pass

    # 傅里叶变换
    def Fourier_transformation(self):
        pass

    # 色彩空间转换
    def HSI_conversion(self):
        pass

    def HSV_conversion(self):
        pass

    # 灰度图转彩色图
    def Gray_image_to_color_image(self):
        pass

    # 图像分割
    def image_segmentation(self):
        pass

    # 边缘检测
    def edge_detection(self):
        pass

    # 目标检测
    def object_detection(self):
        pass

    # 动物识别
    def animal_recognition(self):
        pass

    # 植物识别
    def plant_recognition(self):
        pass

    # 昆虫识别
    def insect_recognition(self):
        pass

    # 证件照换背景
    def id_photo_background_change(self):
        pass

    # 图像超分
    def image_super_resolution(self):
        pass

    # 图像压缩
    def image_compression(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("数字图像处理软件")
    root.geometry("1200x800")
    root.config(background="blue")
    main_page = MainPage(root)
    root.mainloop()
