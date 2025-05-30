import os
import sys
import subprocess
import shutil
import tempfile
from urllib.request import urlretrieve
import zipfile

def download_file(url, dest_file):
    """下载文件到指定目录"""
    print(f"从 {url} 下载文件到 {dest_file}")
    try:
        urlretrieve(url, dest_file)
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False

def main():
    print("=== Python自动安装与配置工具 ===")
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建临时目录
    temp_dir = os.path.join(current_dir, "temp_setup")
    os.makedirs(temp_dir, exist_ok=True)
    
    # 下载Python便携版（嵌入式版本）
    python_zip = os.path.join(temp_dir, "python39.zip")
    success = download_file(
        "https://www.python.org/ftp/python/3.9.13/python-3.9.13-embed-amd64.zip", 
        python_zip
    )
    
    if not success:
        print("无法下载Python，请检查网络连接")
        return
    
    # 创建目标Python目录
    python_dir = os.path.join(current_dir, "python39")
    os.makedirs(python_dir, exist_ok=True)
    
    # 解压Python
    print(f"解压Python到 {python_dir}")
    with zipfile.ZipFile(python_zip, 'r') as zip_ref:
        zip_ref.extractall(python_dir)
    
    # 下载get-pip.py
    pip_py = os.path.join(temp_dir, "get-pip.py")
    success = download_file(
        "https://bootstrap.pypa.io/get-pip.py",
        pip_py
    )
    
    if not success:
        print("无法下载pip安装脚本，请检查网络连接")
        return
    
    # 安装pip
    print("安装pip...")
    python_exe = os.path.join(python_dir, "python.exe")
    subprocess.run([python_exe, pip_py])
    
    # 安装依赖包
    print("安装必要的依赖包...")
    subprocess.run([
        os.path.join(python_dir, "Scripts", "pip.exe"),
        "install",
        "PyQt5", "python-docx", "pillow", "requests"
    ])
    
    # 创建启动脚本
    print("创建启动脚本...")
    with open(os.path.join(current_dir, "run_app.bat"), "w") as f:
        f.write(f"""@echo off
echo 启动物理题目管理系统...
set PATH={python_dir};{os.path.join(python_dir, 'Scripts')};%PATH%
set PYTHONPATH={current_dir}
set PYTHONNOUSERSITE=1
"{python_exe}" "{os.path.join(current_dir, 'gui.py')}"
pause
""")
    
    # 清理临时文件
    print("清理临时文件...")
    shutil.rmtree(temp_dir)
    
    print("""
========== 安装完成 ==========
请双击run_app.bat启动程序
============================
""")

if __name__ == "__main__":
    main() 