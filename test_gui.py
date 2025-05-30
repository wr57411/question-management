import sys
import os

# 测试GUI是否能正常启动
print("开始测试GUI...")

try:
    # 导入必要的模块
    from PyQt5.QtWidgets import QApplication
    print("✓ PyQt5.QtWidgets 导入成功")
    
    # 测试创建应用程序
    app = QApplication(sys.argv)
    print("✓ QApplication 创建成功")
    
    # 导入主窗口
    from gui import PhysicsQuestionGUI
    print("✓ PhysicsQuestionGUI 导入成功")
    
    # 创建主窗口
    window = PhysicsQuestionGUI()
    print("✓ 主窗口创建成功")
    
    # 显示窗口
    window.show()
    print("✓ 窗口显示成功")
    
    print("\n物理题目管理系统已成功启动！")
    print("如果看不到窗口，请检查任务栏或Alt+Tab切换窗口")
    
    # 运行应用
    sys.exit(app.exec_())
    
except Exception as e:
    print(f"\n✗ 错误: {str(e)}")
    import traceback
    traceback.print_exc() 