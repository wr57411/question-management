@echo off
chcp 65001
echo 启动物理题目管理系统简易版...

set PATH=%CD%\local_python;%CD%\local_python\Scripts;%PATH%
set PYTHONPATH=%CD%
set PYTHONNOUSERSITE=1

echo 确保已启动后端服务 (start_backend.bat)

"%CD%\local_python\python.exe" "%CD%\gui_simple.py"

pause 