import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class SimpleTextLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("简易文本记录器")
        self.root.geometry('400x100')  # 固定大小
        self.root.attributes('-alpha', 0.9)  # 设置透明度
        
        # 文本框
        self.entry = tk.Entry(root, font=('Helvetica', 16))
        self.entry.pack(side=tk.LEFT, padx=20, pady=20)
        self.entry.bind('<Return>', self.submit_text)
        
        # 指示灯
        self.canvas = tk.Canvas(root, width=50, height=50)
        self.light = self.canvas.create_oval(10, 10, 40, 40, fill="gray")
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.open_today_file)
    
    def submit_text(self, event=None):
        text = self.entry.get().strip()
        if text:
            self.flash_light('green')
            self.save_to_file(text)
            self.entry.delete(0, 'end')
        else:
            self.flash_light('red')
    
    def flash_light(self, color):
        self.canvas.itemconfig(self.light, fill=color)
        self.root.after(200, lambda: self.canvas.itemconfig(self.light, fill='gray'))
    
    def save_to_file(self, text):
        now = datetime.now()
        week_number = now.isocalendar()[1]
        weekday = str(now.weekday())  # 使用weekday()方法，返回的0是星期一，6是星期天
        if weekday == '6':  # 将星期天设为0
            weekday = '0'
        else:
            weekday = str(int(weekday) + 1)  # 调整为星期一为1，星期二为2...
        
        folder_path = now.strftime(f"%Y-W{week_number}")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        filename = now.strftime(f"%Y-%m-%d W{week_number}-{weekday}.txt")
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "a", encoding='utf-8') as file:  # 确保以UTF-8编码打开
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"- {timestamp} {text}\n")

    def open_today_file(self, event=None):
        now = datetime.now()
        week_number = now.isocalendar()[1]
        weekday = str(now.weekday())
        if weekday == '6':
            weekday = '0'
        else:
            weekday = str(int(weekday) + 1)
        
        folder_path = now.strftime(f"%Y-W{week_number}")
        filename = now.strftime(f"%Y-%m-%d W{week_number}-{weekday}.txt")
        file_path = os.path.join(folder_path, filename)
        
        if os.path.exists(file_path):
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile(file_path)
                elif os.name == 'posix':  # For MacOS and Linux
                    os.system(f'open "{file_path}"')
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件：{e}")
        else:
            messagebox.showwarning("警告", "今天的文件尚未创建。")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTextLogger(root)
    root.mainloop()