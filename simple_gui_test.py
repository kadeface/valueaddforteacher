#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time

class SimpleTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("简单测试GUI")
        self.root.geometry("600x400")
        
        # 强制刷新
        self.root.update()
        
        # 创建主框架
        main_frame = tk.Frame(root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title = tk.Label(main_frame, text="GUI测试程序", font=("Arial", 18, "bold"), bg="white", fg="black")
        title.pack(pady=(0, 30))
        
        # 文件选择
        file_frame = tk.Frame(main_frame, bg="white")
        file_frame.pack(fill=tk.X, pady=10)
        
        file_label = tk.Label(file_frame, text="选择文件:", bg="white", fg="black")
        file_label.pack(side=tk.LEFT)
        
        self.file_path = tk.StringVar(value="未选择文件")
        file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=40)
        file_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        browse_button = tk.Button(file_frame, text="浏览", command=self.browse_file, bg="lightblue")
        browse_button.pack(side=tk.LEFT)
        
        # 按钮
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=30)
        
        test1_button = tk.Button(button_frame, text="测试按钮1", command=self.test1, bg="lightgreen")
        test1_button.pack(side=tk.LEFT, padx=10)
        
        test2_button = tk.Button(button_frame, text="测试按钮2", command=self.test2, bg="lightgreen")
        test2_button.pack(side=tk.LEFT, padx=10)
        
        quit_button = tk.Button(button_frame, text="退出", command=root.quit, bg="lightcoral")
        quit_button.pack(side=tk.LEFT, padx=10)
        
        # 文本区域
        text_frame = tk.Frame(main_frame, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        text_label = tk.Label(text_frame, text="日志输出:", bg="white", fg="black")
        text_label.pack(anchor=tk.W)
        
        self.text_area = tk.Text(text_frame, height=10, width=60, bg="lightyellow", fg="black")
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # 添加初始文本
        self.text_area.insert(tk.END, "GUI测试程序已启动\n")
        self.text_area.insert(tk.END, "请点击按钮测试功能\n")
        
        # 强制更新显示
        self.root.update()
        time.sleep(0.1)
        self.root.update()
        
    def browse_file(self):
        filename = filedialog.askopenfilename(title="选择文件")
        if filename:
            self.file_path.set(filename)
            self.text_area.insert(tk.END, f"已选择文件: {filename}\n")
    
    def test1(self):
        self.text_area.insert(tk.END, "测试按钮1被点击了！\n")
        messagebox.showinfo("信息", "测试按钮1工作正常！")
    
    def test2(self):
        self.text_area.insert(tk.END, "测试按钮2被点击了！\n")
        messagebox.showinfo("信息", "测试按钮2工作正常！")

def main():
    root = tk.Tk()
    
    # 设置环境变量抑制警告
    import os
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    app = SimpleTestGUI(root)
    
    # 确保窗口显示
    root.deiconify()
    root.lift()
    root.focus_force()
    
    root.mainloop()

if __name__ == "__main__":
    main()
