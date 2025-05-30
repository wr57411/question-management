# 物理题目管理系统 - 后端服务启动脚本

# 设置控制台输出编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前工作目录
$currentDir = Get-Location
Write-Host "当前工作目录: $currentDir"

# 使用本地Python解释器
$pythonPath = Join-Path $currentDir "local_python\python.exe"
Write-Host "使用Python路径: $pythonPath"

# 启动后端服务
Write-Host "正在启动物理题目管理系统后端服务..."
& $pythonPath -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload 