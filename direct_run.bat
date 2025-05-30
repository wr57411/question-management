@echo off
echo 尝试直接使用Python310运行程序...

set PATH=C:\Users\wangw\AppData\Local\Programs\Python\Python310\;C:\Users\wangw\AppData\Local\Programs\Python\Python310\Scripts\;%PATH%
set PYTHONPATH=%CD%

echo 当前PATH环境变量的前几项:
echo %PATH:~0,500%

echo 检查Python310是否可用:
C:\Users\wangw\AppData\Local\Programs\Python\Python310\python.exe --version

echo 运行程序:
C:\Users\wangw\AppData\Local\Programs\Python\Python310\python.exe gui.py

if errorlevel 1 (
    echo 程序运行失败，错误代码: %errorlevel%
    echo 尝试安装依赖:
    C:\Users\wangw\AppData\Local\Programs\Python\Python310\python.exe -m pip install PyQt5 python-docx pillow requests
    echo 再次尝试运行:
    C:\Users\wangw\AppData\Local\Programs\Python\Python310\python.exe gui.py
)

echo 程序已结束运行
pause 