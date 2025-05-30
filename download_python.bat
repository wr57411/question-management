@echo off
echo 下载并安装便携版Python...

REM 创建临时目录
mkdir temp_setup 2>nul

REM 下载Python便携版
echo 下载Python便携版...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.13/python-3.9.13-embed-amd64.zip' -OutFile 'temp_setup\python39.zip'}"

REM 下载get-pip.py
echo 下载pip安装脚本...
powershell -Command "& {Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'temp_setup\get-pip.py'}"

REM 创建Python目录
mkdir python39 2>nul

REM 解压Python
echo 解压Python...
powershell -Command "& {Expand-Archive -Path 'temp_setup\python39.zip' -DestinationPath 'python39' -Force}"

REM 配置Python
echo 配置Python...
echo import site >> python39\python39._pth

REM 安装pip
echo 安装pip...
python39\python.exe temp_setup\get-pip.py

REM 安装依赖包
echo 安装依赖包...
python39\Scripts\pip.exe install PyQt5 python-docx pillow requests

REM 创建启动脚本
echo 创建启动脚本...
echo @echo off > run_gui.bat
echo echo 启动物理题目管理系统... >> run_gui.bat
echo set PYTHONPATH=%CD% >> run_gui.bat
echo set PYTHONNOUSERSITE=1 >> run_gui.bat
echo "%CD%\python39\python.exe" "%CD%\gui.py" >> run_gui.bat
echo pause >> run_gui.bat

REM 清理临时文件
echo 清理临时文件...
rmdir /S /Q temp_setup

echo ========== 安装完成 ==========
echo 请双击run_gui.bat启动程序
echo ============================

pause 