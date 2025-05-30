@echo off
echo 启动Python环境修复工具...

:: 尝试使用用户的Python310
if exist "C:\Users\wangw\AppData\Local\Programs\Python\Python310\python.exe" (
    echo 使用用户的Python310运行修复工具...
    C:\Users\wangw\AppData\Local\Programs\Python\Python310\python.exe fix_python_env.py
    goto :end
)

:: 尝试使用虚拟环境
if exist ".venv\Scripts\python.exe" (
    echo 使用虚拟环境的Python运行修复工具...
    .venv\Scripts\python.exe fix_python_env.py
    goto :end
)

echo 未找到可用的Python解释器，无法运行修复工具
echo 请手动修复环境变量：
echo 1. 打开"控制面板" -> "系统" -> "高级系统设置" -> "环境变量"
echo 2. 在"用户变量"中找到"Path"
echo 3. 编辑并移除包含"Python313"的条目
echo 4. 添加"C:\Users\wangw\AppData\Local\Programs\Python\Python310\"
echo 5. 添加"C:\Users\wangw\AppData\Local\Programs\Python\Python310\Scripts\"
echo 6. 确认并重启计算机

:end
echo 操作完成
pause 