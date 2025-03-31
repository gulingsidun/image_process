import tkinter as tk
from distutils.dist import command_re
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class ParameterFrame:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, borderwidth=2, relief=tk.SUNKEN, bg="white")
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        self.params = {}
        self.param_vars = {}

    def clear_params(self):
        # 清空参数区域
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.param_vars = {}

    def set_params(self, params):
        self.clear_params()
        self.params = params

        # 创建一个水平滚动框架，以支持横向排列
        canvas = tk.Canvas(self.frame, bg="white")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建一个水平滚动条
        scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # 配置画布以支持滚动
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # 创建一个内部框架，用于放置参数控件
        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        for i, (key, value) in enumerate(params.items()):
            # 创建参数标签
            label = tk.Label(inner_frame, text=f"{value['label']}:")
            label.pack(side=tk.LEFT, padx=5, pady=5)

            # 根据参数类型创建不同的输入控件
            if value['type'] == 'entry':
                var = tk.StringVar()
                if 'default' in value:
                    var.set(str(value['default']))
                entry = tk.Entry(inner_frame, textvariable=var, width=10)
                entry.pack(side=tk.LEFT, padx=5, pady=5)
                self.param_vars[key] = var
            elif value['type'] == 'scale':
                var = tk.DoubleVar() if 'float' in value else tk.IntVar()
                if 'default' in value:
                    var.set(value['default'])
                scale = tk.Scale(
                    inner_frame,
                    variable=var,
                    from_=value['range'][0],
                    to=value['range'][1],
                    orient=tk.HORIZONTAL,
                    length=150
                )
                scale.pack(side=tk.LEFT, padx=5, pady=5)
                self.param_vars[key] = var

        # 添加应用按钮
        apply_button = tk.Button(inner_frame, text="应用", command=self.get_params)
        apply_button.pack(side=tk.LEFT, padx=5, pady=5)

    def get_params(self):
        params = {}
        for key, var in self.param_vars.items():
            if isinstance(var, tk.StringVar):
                params[key] = var.get()
            elif isinstance(var, tk.IntVar):
                params[key] = var.get()
            elif isinstance(var, tk.DoubleVar):
                params[key] = var.get()
        return params
