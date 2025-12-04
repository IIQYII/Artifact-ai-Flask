#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的文物讲解API测试程序
输入文物信息，返回AI生成的讲解文案
"""

import requests
import json

def test_artifact_api():
    """
    简单的API测试函数
    """
    # API端点
    api_url = "http://localhost:5000/api/artifact-narration"
    
    print("=== 文物讲解API测试 ===")
    print("请输入文物信息进行测试")
    print("-" * 30)
    
    # 获取用户输入
    name = input("请输入文物名称（例如：兵马俑）: ").strip()
    dynasty = input("请输入文物朝代（例如：秦朝）: ").strip()
    
    if not name or not dynasty:
        print("文物名称和朝代都不能为空！")
        return
    
    # 准备请求数据
    data = {
        "name": name,
        "dynasty": dynasty
    }
    
    print(f"\n正在生成 {dynasty} 的 {name} 讲解文案...")
    
    try:
        # 发送POST请求
        response = requests.post(api_url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("生成成功！")
                print("-" * 40)
                print(f"文物: {result['data']['name']}")
                print(f"朝代: {result['data']['dynasty']}")
                print("\n讲解文案:")
                print("-" * 40)
                print(result['data']['narration'])
                print("-" * 40)
            else:
                print(f"生成失败: {result.get('error', '未知错误')}")
                
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("无法连接到服务器，请确保服务器正在运行")
        print("运行命令: python app.py")
        
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
        
    except Exception as e:
        print(f"发生错误: {e}")

def main():
    """
    主函数
    """
    try:
        test_artifact_api()
        
        # 询问是否继续测试
        while True:
            print("\n是否继续测试其他文物？(y/n): ", end="")
            choice = input().strip().lower()
            
            if choice in ['y', 'yes', '是']:
                test_artifact_api()
            elif choice in ['n', 'no', '否']:
                print("感谢使用！")
                break
            else:
                print("请输入 y(是) 或 n(否)")
                
    except KeyboardInterrupt:
        print("\n\n程序已退出")

if __name__ == "__main__":
    main()
