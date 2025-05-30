@echo off
echo 启动物理题目管理系统...
echo 当前目录: %CD%

:: 输出PATH环境变量
echo 当前PATH环境变量:
echo %PATH%

:: 先尝试运行修复脚本
echo 运行Python环境修复脚本...

:: 尝试使用多种可能的Python
if exist ".venv\Scripts\python.exe" (
    echo 使用.venv中的Python...
    .venv\Scripts\python.exe run_app.py
    goto :end
)

if exist "venv\Scripts\python.exe" (
    echo 使用venv中的Python...
    venv\Scripts\python.exe run_app.py
    goto :end
)

:: 尝试直接使用系统Python
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo 使用系统Python...
    python run_app.py
    goto :end
)

:: 尝试直接运行GUI（如果上面都失败）
echo 所有自动修复尝试都失败，直接尝试运行GUI...
if exist ".venv\Scripts\python.exe" (
    echo 直接使用.venv运行GUI...
    .venv\Scripts\python.exe gui.py
    goto :end
)

:: 最后的提示
echo ======================================
echo 无法启动程序，可能是以下原因：
echo 1. 未安装Python或Python路径有问题
echo 2. 环境变量设置错误
echo 
echo 请手动执行以下步骤：
echo 1. 安装Python 3.10或更高版本
echo 2. 检查系统和用户环境变量，移除错误的Python路径
echo 3. 安装所需的依赖包：pip install PyQt5 python-docx pillow requests
echo ======================================

:end
echo 程序已结束运行
pause 