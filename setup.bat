@echo off
chcp 65001
echo ===== 安装便携版Python和依赖 =====

echo 创建临时目录...
mkdir temp_python 2>nul

echo 下载Python便携版...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.13/python-3.9.13-embed-amd64.zip' -OutFile 'temp_python\python39.zip'}"
if %ERRORLEVEL% NEQ 0 (
    echo 下载失败，请检查网络连接
    pause
    exit /b 1
)

echo 下载pip安装脚本...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'temp_python\get-pip.py'}"
if %ERRORLEVEL% NEQ 0 (
    echo 下载失败，请检查网络连接
    pause
    exit /b 1
)

echo 创建Python目录...
mkdir local_python 2>nul

echo 解压Python...
powershell -Command "& {Expand-Archive -Path 'temp_python\python39.zip' -DestinationPath 'local_python' -Force}"
if %ERRORLEVEL% NEQ 0 (
    echo 解压失败
    pause
    exit /b 1
)

echo 修改Python配置以支持导入模块...
del "local_python\python39._pth" 2>nul

echo 安装pip...
local_python\python.exe temp_python\get-pip.py
if %ERRORLEVEL% NEQ 0 (
    echo pip安装失败
    pause
    exit /b 1
)

echo 安装程序所需的依赖包...
local_python\Scripts\pip.exe install PyQt5 python-docx pillow requests
if %ERRORLEVEL% NEQ 0 (
    echo 依赖包安装失败
    pause
    exit /b 1
)

echo 创建启动脚本...
(
echo @echo off
echo chcp 65001
echo echo 启动物理题目管理系统...
echo.
echo set PYTHONPATH=%%CD%%
echo set PYTHONNOUSERSITE=1
echo.
echo "%%CD%%\local_python\python.exe" "%%CD%%\gui.py"
echo.
echo pause
) > start_program.bat

echo 清理临时文件...
rmdir /s /q temp_python

echo ===== 安装完成 =====
echo 请双击 start_program.bat 启动程序
echo ===================

pause 