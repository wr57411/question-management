import os
import requests
import argparse

def test_import(questions_file: str, answers_file: str = None):
    """测试导入功能
    
    Args:
        questions_file: 题目文档路径
        answers_file: 答案文档路径（可选）
    """
    # 检查文件是否存在
    if not os.path.exists(questions_file):
        print(f"错误：题目文件 {questions_file} 不存在")
        return
        
    if answers_file and not os.path.exists(answers_file):
        print(f"错误：答案文件 {answers_file} 不存在")
        return
    
    # 准备文件
    files = {
        'file': (os.path.basename(questions_file), open(questions_file, 'rb'))
    }
    
    if answers_file:
        files['answer_file'] = (os.path.basename(answers_file), open(answers_file, 'rb'))
    
    try:
        # 发送请求
        print(f"\n正在导入题目文件：{questions_file}")
        if answers_file:
            print(f"正在导入答案文件：{answers_file}")
            
        response = requests.post(
            'http://localhost:8000/api/physics-questions/import-word',
            files=files
        )
        
        # 打印结果
        print("\n导入结果：")
        print(response.json())
        
    except Exception as e:
        print(f"测试失败：{str(e)}")
        
    finally:
        # 关闭文件
        for file in files.values():
            file[1].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='导入物理题目和答案')
    parser.add_argument('questions_file', help='题目Word文档路径')
    parser.add_argument('--answers_file', help='答案Word文档路径（可选）')
    
    args = parser.parse_args()
    test_import(args.questions_file, args.answers_file) 