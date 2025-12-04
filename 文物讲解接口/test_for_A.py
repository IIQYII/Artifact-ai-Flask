"""
给角色A的测试文件
用于验证AI生成模块是否正常工作
"""

from artifact_ai_generator import generate_artifact_story

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 AI文物讲解生成模块测试")
    print("=" * 60)
    
    # 替换成实际的API密钥
    API_KEY = "sk-你的API密钥"  # 角色D会提供这个密钥
    
    # 测试用例
    test_cases = [
        ("兵马俑", "秦朝"),
        ("司母戊鼎", "商朝"),
        ("唐三彩", "唐朝"),
        ("越王勾践剑", "春秋战国"),
        ("四羊方尊", "商朝")
    ]
    
    print("1. 基本功能测试")
    print("-" * 40)
    
    for i, (name, dynasty) in enumerate(test_cases, 1):
        print(f"\n{i}. 测试 {name} ({dynasty})...")
        
        try:
            # 调用AI生成函数
            story = generate_artifact_story(name, dynasty, API_KEY)
            
            print(f"✅ 生成成功！")
            print(f"   文物: {name}")
            print(f"   朝代: {dynasty}")
            print(f"   生成内容: {story}")
            print(f"   内容长度: {len(story)} 字符")
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")

def test_error_handling():
    """测试错误处理"""
    print("\n\n2. 错误处理测试")
    print("-" * 40)
    
    API_KEY = "sk-你的API密钥"
    
    # 测试空值
    print("测试空文物名...")
    try:
        result = generate_artifact_story("", "秦朝", API_KEY)
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试空朝代
    print("\n测试空朝代...")
    try:
        result = generate_artifact_story("兵马俑", "", API_KEY)
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")

def test_performance():
    """测试性能"""
    print("\n\n3. 性能测试")
    print("-" * 40)
    
    API_KEY = "sk-你的API密钥"
    
    import time
    
    start_time = time.time()
    
    try:
        story = generate_artifact_story("兵马俑", "秦朝", API_KEY)
        end_time = time.time()
        
        print(f"✅ 请求成功")
        print(f"   响应时间: {end_time - start_time:.2f} 秒")
        print(f"   内容长度: {len(story)} 字符")
        print(f"   示例内容: {story[:50]}...")
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")

def integration_example():
    """集成示例 - 展示如何在后端中使用"""
    print("\n\n4. 后端集成示例")
    print("-" * 40)
    
    print("""
# 在FastAPI中的使用示例：

from fastapi import FastAPI
from artifact_ai_generator import generate_artifact_story

app = FastAPI()
API_KEY = "sk-你的API密钥"

@app.post("/api/generate-narration")
async def generate_narration(artifact_name: str, artifact_dynasty: str):
    \"""生成文物讲解\"""
    try:
        story = generate_artifact_story(artifact_name, artifact_dynasty, API_KEY)
        return {
            "success": True,
            "data": {
                "artifact_name": artifact_name,
                "artifact_dynasty": artifact_dynasty,
                "narration": story
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 调用方式：
# POST /api/generate-narration
# Body: {"artifact_name": "兵马俑", "artifact_dynasty": "秦朝"}
""")

if __name__ == "__main__":
    # 运行所有测试
    test_basic_functionality()
    test_error_handling() 
    test_performance()
    integration_example()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("如果所有测试都通过，说明AI模块可以正常集成到后端中。")
    print("=" * 60)