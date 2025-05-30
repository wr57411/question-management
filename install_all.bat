@echo off
chcp 65001
echo ===== 物理题目管理系统一键安装与启动 =====

echo 1. 安装后端依赖...
.\local_python\Scripts\pip.exe install fastapi uvicorn sqlalchemy python-docx python-multipart

echo 2. 设置环境变量...
set PATH=%CD%\local_python;%CD%\local_python\Scripts;%PATH%
set PYTHONPATH=%CD%
set PYTHONNOUSERSITE=1

echo 3. 创建后端启动脚本...
(
echo @echo off
echo chcp 65001
echo echo 启动物理题目管理系统后端服务...
echo.
echo set PATH=%%CD%%\local_python;%%CD%%\local_python\Scripts;%%PATH%%
echo set PYTHONPATH=%%CD%%
echo set PYTHONNOUSERSITE=1
echo.
echo echo 当前工作目录: %%CD%%
echo echo 使用Python路径: %%CD%%\local_python\python.exe
echo.
echo "%%CD%%\local_python\Scripts\uvicorn" main:app --host 0.0.0.0 --port 8000
echo.
echo pause
) > start_backend.bat

echo 4. 创建前端启动脚本...
(
echo @echo off
echo chcp 65001
echo echo 启动物理题目管理系统前端...
echo.
echo set PATH=%%CD%%\local_python;%%CD%%\local_python\Scripts;%%PATH%%
echo set PYTHONPATH=%%CD%%
echo set PYTHONNOUSERSITE=1
echo.
echo "%%CD%%\local_python\python.exe" "%%CD%%\gui.py"
echo.
echo pause
) > start_frontend.bat

echo 5. 检查gui.py中的缩进错误...
echo  - 请使用编辑器手动修复gui.py中的缩进错误
echo    特别注意：行号367、466和488附近，需要确保try/except块的正确缩进

echo ===== 安装完成 =====
echo 1. 先运行 start_backend.bat 启动后端服务
echo 2. 再运行 start_frontend.bat 启动前端GUI
echo 3. 如果遇到问题，请修复gui.py中的缩进错误后再试
echo ============================

pause 