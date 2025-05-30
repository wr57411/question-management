# 物理题目管理系统 - 前端GUI启动脚本
Write-Host "启动物理题目管理系统前端GUI..." -ForegroundColor Green

# 设置控制台输出编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前工作目录
$currentDir = Get-Location
Write-Host "当前工作目录: $currentDir"

# 使用本地Python解释器
$pythonPath = Join-Path $currentDir "local_python\python.exe"
Write-Host "使用Python路径: $pythonPath"

Write-Host "确保后端服务已经启动（在另一个终端运行 .\Start-Backend.ps1）" -ForegroundColor Red

# 启动GUI程序
Write-Host "正在启动物理题目管理系统前端..."
& $pythonPath (Join-Path $currentDir "gui.py") 