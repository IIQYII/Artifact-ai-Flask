#!/usr/bin/env python3
"""
图像识别功能整合测试脚本
用于验证图像识别功能是否成功整合到后端项目中
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_artifact_recognizer():
    """测试ArtifactRecognizer类是否能正常初始化"""
    try:
        from api.artifact_recognizer import ArtifactRecognizer
        print("✓ ArtifactRecognizer导入成功")
        
        # 尝试初始化识别器
        recognizer = ArtifactRecognizer()
        print("✓ ArtifactRecognizer初始化成功")
        
        # 检查数据文件是否加载成功
        if hasattr(recognizer, 'candidate_labels') and recognizer.candidate_labels:
            print(f"✓ 候选标签加载成功，共{len(recognizer.candidate_labels)}个标签")
        else:
            print("✗ 候选标签加载失败")
            return False
            
        if hasattr(recognizer, 'artifact_df') and not recognizer.artifact_df.empty:
            print(f"✓ 文物数据加载成功，共{len(recognizer.artifact_df)}条记录")
        else:
            print("✗ 文物数据加载失败")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ ArtifactRecognizer测试失败: {e}")
        return False

def test_image_api():
    """测试image_api是否能正常导入"""
    try:
        from api.image_api import image_api, recognizer
        print("✓ image_api导入成功")
        print("✓ 图像识别器已初始化")
        return True
    except Exception as e:
        print(f"✗ image_api测试失败: {e}")
        return False

def test_data_files():
    """测试数据文件是否存在"""
    data_files = [
        'data/artifact_data.csv',
        'data/candidate_labels.txt'
    ]
    
    all_files_exist = True
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"{file_path} 存在")
        else:
            print(f"{file_path} 不存在")
            all_files_exist = False
            
    return all_files_exist

def main():
    """主测试函数"""
    print("=" * 50)
    print("图像识别功能整合测试")
    print("=" * 50)
    
    # 测试数据文件
    print("\n1. 测试数据文件:")
    data_files_ok = test_data_files()
    
    # 测试ArtifactRecognizer
    print("\n2. 测试ArtifactRecognizer类:")
    recognizer_ok = test_artifact_recognizer()
    
    # 测试image_api
    print("\n3. 测试image_api:")
    api_ok = test_image_api()
    
    # 总结
    print("\n" + "=" * 50)
    print("整合测试结果:")
    print(f"数据文件: {'✓ 通过' if data_files_ok else '✗ 失败'}")
    print(f"识别器类: {'✓ 通过' if recognizer_ok else '✗ 失败'}")
    print(f"API模块: {'✓ 通过' if api_ok else '✗ 失败'}")
    
    if data_files_ok and recognizer_ok and api_ok:
        print("\n图像识别功能整合成功！")
        print("\n下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 启动服务器: python app.py")
        print("3. 访问 http://localhost:5000 测试图像识别功能")
    else:
        print("\n整合测试失败，请检查上述错误信息")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
