import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

from baiduimage import baidu_get_image_url_using_api, download_images
from glm_image import generate_and_save_images_multithreaded

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('图片下载器')
        self.geometry("400x350")
        
        self.label_keywords = tk.Label(self, text="主题:")
        self.entry_keywords = tk.Entry(self)
        
        self.label_max_number = tk.Label(self, text="下载图片数量:")
        self.entry_max_number = tk.Entry(self)
        
        self.button_select_folder = tk.Button(self, text="选择保存位置", command=self.select_folder)
        self.label_selected_folder = tk.Label(self, text="")
        
        self.button_confirm = tk.Button(self, text="确认", command=self.confirm)
        
        self.label_keywords.pack()
        self.entry_keywords.pack()
        self.label_max_number.pack()
        self.entry_max_number.pack()
        self.button_select_folder.pack()
        self.label_selected_folder.pack()
        
        # 添加单选框
        self.var_method = tk.StringVar(value="none")  # 默认值为"none"
        
        # 使用Frame来组织单选框
        self.frame_radiobuttons = tk.Frame(self)
        self.radiobutton_crawler = tk.Radiobutton(self.frame_radiobuttons, text="使用爬虫", variable=self.var_method, value="crawler")
        self.radiobutton_ai = tk.Radiobutton(self.frame_radiobuttons, text="使用AI", variable=self.var_method, value="ai")
        
        self.radiobutton_crawler.pack(side="left", padx=10)
        self.radiobutton_ai.pack(side="left", padx=10)
        self.frame_radiobuttons.pack()
        
        self.button_confirm.pack()

        # 添加一个标签来显示软件作者公众号信息
        self.label_author = tk.Label(self, text="软件作者公众号：与龙邂逅", fg="blue", cursor="hand2")
        self.label_author.pack(side="bottom", pady=10)  # 使用side和pady来调整标签的位置

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.label_selected_folder.config(text=folder_path)

    def confirm(self):
        keywords = self.entry_keywords.get()
        max_number = int(self.entry_max_number.get())
        save_folder = self.label_selected_folder.cget("text")
        
        if not save_folder or not os.path.isdir(save_folder):
            messagebox.showerror("错误", "请选择有效的保存文件夹！")
            return
        
        try:
            method = self.var_method.get()
            if method == "crawler":
                urls = baidu_get_image_url_using_api(keywords, max_number=max_number)
                download_images(urls, save_folder, keywords, timeout=20)
            elif method == "ai":
                generate_and_save_images_multithreaded(keywords, max_number, save_folder)
            else:
                messagebox.showerror("错误", "请选择一种下载方式！")
                return

            messagebox.showinfo("完成", "图片已成功下载！")
            self.open_folder(save_folder)
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def open_folder(self, path):
        if os.name == 'nt':  # for Windows
            os.startfile(path)
        elif os.name == 'posix':  # for Linux, Mac, etc.
            opener = 'open' if os.uname().sysname == 'Darwin' else 'xdg-open'
            subprocess.call([opener, path])

if __name__ == "__main__":
    app = App()
    app.mainloop()