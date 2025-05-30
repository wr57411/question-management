import sys
import os
import requests
import json
import tkinter as tk
from tkinter import filedialog, messagebox, Text, Button, Label, Frame, Scrollbar

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("物理题目管理系统简易版")
        self.root.geometry("800x600")
        
        self.file_path = None
        
        # 创建主框架
        main_frame = Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 上传按钮
        upload_button = Button(main_frame, text="上传题目文档", command=self.upload_file)
        upload_button.pack(pady=10)
        
        # 显示选择的文件
        self.file_label = Label(main_frame, text="未选择文件")
        self.file_label.pack(pady=5)
        
        # 答案输入框
        Label(main_frame, text="在下方输入答案（格式：题号,答案,解析）：").pack(anchor=tk.W, pady=5)
        
        # 添加带滚动条的文本框
        text_frame = Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.answer_text = Text(text_frame, height=15, width=80)
        self.answer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.answer_text.yview)
        self.answer_text.config(yscrollcommand=scrollbar.set)
        
        # 提交按钮
        submit_button = Button(main_frame, text="提交", command=self.submit)
        submit_button.pack(pady=10)
        
        # 显示结果
        result_frame = Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        Label(result_frame, text="结果：").pack(anchor=tk.W)
        
        result_scrollbar = Scrollbar(result_frame)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = Text(result_frame, height=10, width=80)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        result_scrollbar.config(command=self.result_text.yview)
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
    def upload_file(self):
        """上传文件"""
        file_path = filedialog.askopenfilename(
            title="选择题目文档",
            filetypes=[("Word Files", "*.docx"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=f"已选择文件: {os.path.basename(file_path)}")
        
    def submit(self):
        """提交数据到后端"""
        if not self.file_path:
            messagebox.showwarning("警告", "请先上传题目文档")
            return
        
        answer_text = self.answer_text.get("1.0", tk.END).strip()
        if not answer_text:
            messagebox.showwarning("警告", "请输入答案内容")
            return
        
        try:
            # 准备文件和数据
            with open(self.file_path, "rb") as file:
                files = {
                    'file': (os.path.basename(self.file_path), file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                }
                data = {
                    'answer_text': answer_text,
                    'gui_mode': 'true'
                }
                
                # 发送请求
                response = requests.post(
                    'http://localhost:8000/api/physics-questions/import-word',
                    files=files,
                    data=data
                )
                
                # 显示结果
                if response.status_code == 200:
                    try:
                        result = response.json()
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert(tk.END, f"成功: {result.get('message', '答案已成功提交')}")
                        messagebox.showinfo("成功", result.get('message', '答案已成功提交'))
                    except json.JSONDecodeError:
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert(tk.END, "成功: 答案已成功提交")
                        messagebox.showinfo("成功", "答案已成功提交")
                else:
                    try:
                        error_detail = response.json().get('detail', '未知错误')
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert(tk.END, f"错误: {error_detail}")
                        messagebox.showerror("错误", f"上传失败：{error_detail}")
                    except json.JSONDecodeError:
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert(tk.END, f"错误: HTTP {response.status_code}")
                        messagebox.showerror("错误", f"上传失败：HTTP {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "错误: 无法连接到服务器")
            messagebox.showerror("错误", "无法连接到服务器，请确保后端服务已启动")
        except Exception as e:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"错误: {str(e)}")
            messagebox.showerror("错误", f"上传失败：{str(e)}")

def main():
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 