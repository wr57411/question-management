@echo off
chcp 65001
echo 启动物理题目管理系统...

set PYTHONPATH=%CD%
set PYTHONNOUSERSITE=1

"%CD%\local_python\python.exe" "%CD%\gui.py"

pause
