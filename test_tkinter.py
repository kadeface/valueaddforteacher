#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("Tkinter测试")
    root.geometry("400x300")
    
    # 创建标签
    label = ttk.Label(root, text="Hello, Tkinter!")
    label.pack(pady=20)
    
    # 创建按钮
    button = ttk.Button(root, text="点击我", command=lambda: print("按钮被点击了！"))
    button.pack(pady=10)
    
    # 创建输入框
    entry = ttk.Entry(root)
    entry.pack(pady=10)
    entry.insert(0, "输入一些文字")
    
    # 创建文本区域
    text = tk.Text(root, height=5, width=30)
    text.pack(pady=10)
    text.insert(tk.END, "这是一个文本区域\n可以输入多行文字")
    
    print("Tkinter测试程序启动成功！")
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()
