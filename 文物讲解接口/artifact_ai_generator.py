import dashscope
from dashscope import Generation

class ArtifactAIGenerator:
    def __init__(self, api_key):
        """
        初始化AI生成器
        :param api_key: 阿里云API密钥 (格式: sk-xxxxxxxx)
        """
        dashscope.api_key = api_key
        self.model = 'qwen-turbo'
    
    def generate_narration(self, artifact_name, artifact_dynasty):
        """
        生成文物讲解文案的主要函数
        :param artifact_name: 文物名称 (如 "兵马俑")
        :param artifact_dynasty: 文物朝代 (如 "秦朝") 
        :return: 生成的第一人称讲解文案
        """
        prompt = f"""
你是一个专业的博物馆讲解员。请为以下文物创作一段第一人称的讲解：

文物：{artifact_name}
朝代：{artifact_dynasty}

要求：
1. 严格使用第一人称"我"
2. 内容符合历史事实
3. 语言生动专业，吸引游客
4. 字数150-200字

请直接输出讲解内容。
"""
        
        try:
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            
            if response.status_code == 200:
                story = response.output.text.strip()
                # 清理输出
                if story.startswith('"') and story.endswith('"'):
                    story = story[1:-1]
                return story
            else:
                return f"生成失败，请稍后重试。错误码：{response.status_code}"
                
        except Exception as e:
            return f"系统繁忙，请稍后重试。错误：{str(e)}"

# 给角色A使用的主要函数
def generate_artifact_story(artifact_name, artifact_dynasty, api_key):
    """
    生成文物讲解文案
    这是给后端调用的主要接口函数
    
    参数:
        artifact_name (str): 文物名称
        artifact_dynasty (str): 文物朝代  
        api_key (str): 阿里云API密钥
    
    返回:
        str: 生成的讲解文案
    """
    generator = ArtifactAIGenerator(api_key)
    return generator.generate_narration(artifact_name, artifact_dynasty)