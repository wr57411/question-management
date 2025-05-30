import os
import sys
import subprocess
import ctypes
import traceback
import shutil
import winreg

def is_admin():
    """检查当前用户是否有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def update_registry_path(key_type, remove_patterns=None, add_paths=None):
    """更新注册表中的PATH环境变量
    
    Args:
        key_type: 'user' 或 'system'，表示更新用户或系统环境变量
        remove_patterns: 要从PATH中移除的字符串模式列表，如 ['Python313']
        add_paths: 要添加到PATH的路径列表
    """
    if key_type == 'user':
        key = winreg.HKEY_CURRENT_USER
        subkey = 'Environment'
    else:  # system
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    
    try:
        # 打开注册表键
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ | winreg.KEY_WRITE) as reg_key:
            # 获取当前PATH值
            current_path, _ = winreg.QueryValueEx(reg_key, 'Path')
            print(f"当前{key_type} PATH: {current_path}")
            
            # 分割PATH为列表
            path_parts = current_path.split(';')
            new_parts = []
            
            # 过滤掉要移除的模式
            if remove_patterns:
                for part in path_parts:
                    should_keep = True
                    for pattern in remove_patterns:
                        if pattern in part:
                            print(f"移除路径: {part}")
                            should_keep = False
                            break
                    if should_keep:
                        new_parts.append(part)
            else:
                new_parts = path_parts
            
            # 添加新路径
            if add_paths:
                for path in add_paths:
                    if path and path not in new_parts:
                        print(f"添加路径: {path}")
                        new_parts.append(path)
            
            # 重新组合PATH
            new_path = ';'.join(filter(None, new_parts))
            print(f"新的{key_type} PATH: {new_path}")
            
            # 更新注册表
            winreg.SetValueEx(reg_key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"成功更新{key_type} PATH环境变量")
            
            return True
    except Exception as e:
        print(f"更新{key_type} PATH环境变量失败: {str(e)}")
        traceback.print_exc()
        return False

def check_and_fix_python_environment():
    """检查并修复Python环境变量"""
    try:
        print("===== 检查并修复Python环境 =====")
        
        # 检查当前环境变量中的Python
        path = os.environ.get('PATH', '')
        
        # 检查Python313引用是否存在于环境变量中
        has_python313 = 'Python313' in path
        if has_python313:
            print("警告: 环境变量中包含无效的Python313引用")
        
        # 查找当前系统中所有可用的Python安装
        python_installations = []
        
        # 检查常见的Python安装路径
        common_paths = [
            r'C:\Python310',
            r'C:\Python311',
            r'C:\Python39',
            r'C:\Python312',
            r'C:\Program Files\Python310',
            r'C:\Program Files\Python311',
            r'C:\Users\wangw\AppData\Local\Programs\Python\Python310',
            r'C:\Users\wangw\AppData\Local\Programs\Python\Python311'
        ]
        
        for p in common_paths:
            python_exe = os.path.join(p, 'python.exe')
            if os.path.exists(python_exe):
                python_installations.append(p)
                print(f"找到Python安装: {p}")
        
        # 如果没有找到Python安装，尝试在PATH中查找
        if not python_installations:
            python_path = shutil.which('python')
            if python_path:
                python_dir = os.path.dirname(python_path)
                python_installations.append(python_dir)
                print(f"在PATH中找到Python: {python_dir}")
        
        if not python_installations:
            print("未找到任何Python安装，请安装Python 3.x")
            return False
        
        # 准备修复操作
        if has_python313 or not python_installations:
            if is_admin():
                print("检测到管理员权限，将尝试修复系统和用户环境变量")
                
                # 修复系统环境变量
                if has_python313:
                    update_registry_path('system', remove_patterns=['Python313'])
                
                # 修复用户环境变量
                if has_python313:
                    update_registry_path('user', remove_patterns=['Python313'])
                
                # 添加有效的Python路径到用户环境变量
                if python_installations:
                    for install_path in python_installations:
                        scripts_path = os.path.join(install_path, 'Scripts')
                        update_registry_path('user', add_paths=[install_path, scripts_path])
                
                print("已更新环境变量，需要重启计算机才能生效")
                return True
            else:
                print("无管理员权限，无法更新注册表")
                print("请右键点击此脚本，选择'以管理员身份运行'")
                return False
        else:
            print("Python环境变量看起来正常，无需修复")
            return True
    
    except Exception as e:
        print(f"检查Python环境时出错: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Python环境修复工具")
    print("此工具将检查并修复Python环境变量问题")
    
    if is_admin():
        print("以管理员权限运行")
    else:
        print("警告: 未以管理员权限运行，某些操作可能受限")
        print("建议右键点击此脚本，选择'以管理员身份运行'")
    
    result = check_and_fix_python_environment()
    
    if result:
        print("\n环境检查完成！")
        if is_admin():
            print("请重启计算机，然后尝试运行程序")
        else:
            print("为了应用所有更改，建议重启计算机")
    else:
        print("\n环境检查发现问题，请查看上面的消息")
    
    input("按回车键退出...") 