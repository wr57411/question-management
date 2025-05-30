import os
import sys
import subprocess
import traceback

print("启动物理题目管理系统自动修复工具...")

def fix_path_environment():
    """修复PATH环境变量"""
    # 同时检查系统变量和用户变量的PATH
    path = os.environ.get("PATH", "")
    print(f"当前PATH环境变量: {path}")
    
    # 检查是否存在C:\Python313\python.exe的引用
    if "Python313" in path:
        print("检测到错误的Python路径(Python313)，尝试修复...")
        path_parts = path.split(";")
        new_path_parts = [p for p in path_parts if "Python313" not in p]
        os.environ["PATH"] = ";".join(new_path_parts)
        print("已从PATH中移除错误的Python路径")
    
    # 确保Python310路径正确存在于PATH中
    if "Python310" in path and not os.path.exists("C:\\Python310\\python.exe"):
        print("检测到可能错误的Python310路径，但实际文件不存在...")
        path_parts = path.split(";")
        
        # 检查每个包含Python310的路径是否实际存在
        for i, part in enumerate(path_parts):
            if "Python310" in part and not os.path.exists(os.path.join(part, "python.exe")):
                print(f"移除不存在的Python路径: {part}")
                path_parts[i] = ""  # 标记为空，后面会过滤掉
        
        # 过滤掉空路径
        new_path_parts = [p for p in path_parts if p]
        os.environ["PATH"] = ";".join(new_path_parts)
        print("已更新PATH环境变量")
    
    return True

def find_python_executable():
    """查找可用的Python解释器"""
    potential_paths = [
        ".venv/Scripts/python.exe",
        ".venv\\Scripts\\python.exe",
        "venv/Scripts/python.exe",
        "venv\\Scripts\\python.exe",
        "Python310Portable/python.exe",
        "Python310Portable\\python.exe",
        "C:/Python310/python.exe",
        "C:\\Python310\\python.exe",
        "C:/Python39/python.exe",
        "C:\\Python39\\python.exe",
        "C:/Python311/python.exe",
        "C:\\Python311\\python.exe",
        "C:/Python312/python.exe",
        "C:\\Python312\\python.exe"
    ]
    
    # 首先检查环境变量指向的Python
    try:
        import shutil
        python_in_path = shutil.which("python")
        if python_in_path:
            print(f"在PATH中找到Python: {python_in_path}")
            return python_in_path
    except Exception as e:
        print(f"检查PATH中的Python时出错: {str(e)}")
    
    # 然后检查列表中的路径
    for path in potential_paths:
        if os.path.exists(path):
            abs_path = os.path.abspath(path)
            print(f"找到可用的Python解释器: {abs_path}")
            return abs_path
    
    print("未找到可用的Python解释器")
    return None

def main():
    try:
        # 修复环境变量
        fix_path_environment()
        
        # 查找Python解释器
        python_exe = find_python_executable()
        if not python_exe:
            print("无法找到可用的Python解释器，请安装Python 3.x")
            input("按任意键退出...")
            return
        
        # 设置环境变量
        os.environ["PYTHONPATH"] = os.path.abspath(".")
        os.environ["QT_QPA_PLATFORM"] = "windows"
        
        # 运行GUI程序
        print(f"使用Python解释器 {python_exe} 运行GUI程序...")
        try:
            result = subprocess.call([python_exe, "gui.py"])
            print(f"程序运行结束，返回代码: {result}")
        except Exception as e:
            print(f"运行GUI程序时出错: {str(e)}")
            traceback.print_exc()
        
    except Exception as e:
        print(f"程序运行时出错: {str(e)}")
        traceback.print_exc()
        input("按任意键退出...")

if __name__ == "__main__":
    main() 