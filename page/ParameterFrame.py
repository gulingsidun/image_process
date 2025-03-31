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
        for i, (key, value) in enumerate(params.items()):
            # 创建参数标签
            label = tk.Label(self.frame, text=f"{value['label']}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

            # 根据参数类型创建不同的输入控件
            if value['type'] == 'entry':
                var = tk.StringVar()
                if 'default' in value:
                    var.set(str(value['default']))
                entry = tk.Entry(self.frame, textvariable=var, width=10)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                self.param_vars[key] = var
            elif value['type'] == 'scale':
                var = tk.DoubleVar() if 'float' in value else tk.IntVar()
                if 'default' in value:
                    var.set(value['default'])
                scale = tk.Scale(
                    self.frame,
                    variable=var,
                    from_=value['range'][0],
                    to=value['range'][1],
                    orient=tk.HORIZONTAL,
                    length=200
                )
                scale.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                self.param_vars[key] = var

        # 添加应用按钮
        apply_button = tk.Button(self.frame, text="应用", command=self.get_params)
        apply_button.grid(row=len(params), column=0, columnspan=2, padx=5, pady=5)

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
