@echo off
chcp 65001
echo 启动物理题目管理系统前端...

set PATH=%CD%\local_python;%CD%\local_python\Scripts;%PATH%
set PYTHONPATH=%CD%
set PYTHONNOUSERSITE=1

"%CD%\local_python\python.exe" "%CD%\gui.py"

pause
