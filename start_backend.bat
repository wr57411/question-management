@echo off
chcp 65001
echo 启动物理题目管理系统后端服务...

set PATH=%CD%\local_python;%CD%\local_python\Scripts;%PATH%
set PYTHONPATH=%CD%
set PYTHONNOUSERSITE=1

echo 当前工作目录: %CD%
echo 使用Python路径: %CD%\local_python\python.exe

"%CD%\local_python\Scripts\uvicorn" main:app --host 0.0.0.0 --port 8000

pause
