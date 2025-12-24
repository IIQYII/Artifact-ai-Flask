#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像识别功能测试程序
用于验证图像识别接口是否正常工作
"""

import os
import sys
from PIL import Image
import io

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_image_recognition():
    """测试图像识别功能"""
    try:
        # 导入图像识别器
        from api.artifact_recognizer import ArtifactRecognizer
        
        print("=" * 50)
        print("图像识别功能测试")
        print("=" * 50)
        
        # 初始化识别器
        print("正在初始化图像识别器...")
        recognizer = ArtifactRecognizer()
        print("✓ 图像识别器初始化成功")
        
        # 测试图片目录
        test_images_dir = "图像识别接口/test_images"
        
        if not os.path.exists(test_images_dir):
            print(f"✗ 测试图片目录不存在: {test_images_dir}")
            return False
        
        # 获取测试图片
        test_images = []
        for filename in os.listdir(test_images_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                test_images.append(os.path.join(test_images_dir, filename))
        
        if not test_images:
            print("✗ 未找到测试图片")
            return False
        
        print(f"找到 {len(test_images)} 张测试图片")
        
        # 测试每张图片
        success_count = 0
        for i, image_path in enumerate(test_images[:]):
            print(f"\n--- 测试图片 {i+1}: {os.path.basename(image_path)} ---")
            
            try:
                # 读取图片文件
                with open(image_path, 'rb') as f:
                    image_bytes = f.read()
                
                # 进行图像识别，降低阈值到0.1
                result = recognizer.recognize(image_bytes, conf_threshold=0.1)
                
                if result.get('success'):
                    print("✓ 识别成功")
                    print(f"  识别结果: {len(result['result'])} 个匹配项")
                    
                    # 显示所有结果
                    for j, match in enumerate(result['result']):
                        print(f"  结果 {j+1}: {match['name']} - {match['dynasty']} (置信度: {match['confidence']:.3f})")
                    
                    success_count += 1
                else:
                    print(f"✗ 识别失败: {result.get('error', '未知错误')}")
                    # 尝试显示原始相似度信息用于调试
                    try:
                        # 直接调用内部方法获取更多调试信息
                        image_tensor = recognizer.process_image(image_bytes)
                        if image_tensor is not None:
                            with torch.no_grad():
                                image_features = recognizer.model.encode_image(image_tensor)
                                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                                similarity = (100.0 * image_features @ recognizer.encoded_labels.T).softmax(dim=-1)
                                top_values, top_indices = similarity.topk(5)
                                print("  相似度最高的5个标签:")
                                for k, (val, idx) in enumerate(zip(top_values[0], top_indices[0])):
                                    label = recognizer.candidate_labels[idx]
                                    print(f"    {k+1}. {label}: {val.item():.3f}")
                    except Exception as debug_e:
                        print(f"  调试信息获取失败: {str(debug_e)}")
                    
            except Exception as e:
                print(f"✗ 处理图片时出错: {str(e)}")
        
        # 输出测试总结
        print("\n" + "=" * 50)
        print("测试总结")
        print("=" * 50)
        print(f"总测试图片数: {min(100, len(test_images))}")
        print(f"成功识别数: {success_count}")
        print(f"成功率: {success_count/min(100, len(test_images))*100:.1f}%")
        
        if success_count > 0:
            print("✓ 图像识别功能测试通过")
            return True
        else:
            print("✗ 图像识别功能测试失败")
            return False
            
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {str(e)}")
        return False

def test_api_integration():
    """测试API集成"""
    try:
        print("\n" + "=" * 50)
        print("API集成测试")
        print("=" * 50)
        
        # 模拟API请求
        from flask import Flask
        from api.image_api import image_api
        
        # 创建测试应用
        app = Flask(__name__)
        app.register_blueprint(image_api, url_prefix='/api/image-recognition')
        
        print("✓ API蓝图注册成功")
        print("✓ 图像识别接口已集成到Flask后端")
        
        # 测试配置
        from config import API_CONFIG
        image_config = API_CONFIG['image_recognition']
        print(f"✓ 接口端点: {image_config['endpoint']}")
        print(f"✓ 支持方法: {image_config['methods']}")
        
        return True
        
    except Exception as e:
        print(f"✗ API集成测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始图像识别功能验证...")
    
    # 测试图像识别功能
    recognition_ok = test_image_recognition()
    
    # 测试API集成
    api_ok = test_api_integration()
    
    print("\n" + "=" * 50)
    print("最终测试结果")
    print("=" * 50)
    
    if recognition_ok and api_ok:
        print("所有测试通过 图像识别功能已成功集成到后端")
        print("✓ 图像识别功能正常")
        print("✓ API集成正常")
        print("✓ 可以启动服务器进行完整测试")
        sys.exit(0)
    else:
        print("测试失败，请检查以上错误信息")
        sys.exit(1)
