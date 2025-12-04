# 配置文件模板
# 请复制此文件为 config.py 并填入您的实际配置信息
# 注意：config.py 文件已被 .gitignore 保护，不会提交到版本控制

# 前端路径配置
FRONTEND_CONFIG = {
    'static_folder': 'static',
    'template_folder': 'templates',
    'allowed_extensions': {'png', 'jpg', 'jpeg', 'gif'}
}

# API接口配置
API_CONFIG = {
    'image_recognition': {
        'endpoint': '/api/image-recognition',
        'methods': ['POST'],
        'description': '图像识别接口 - 输入图片,返回识别结果JSON'
    },
    'artifact_narration': {
        'endpoint': '/api/artifact-narration',
        'methods': ['POST'],
        'description': '文物讲解生成接口 - 输入文物信息,返回AI生成的讲解文案',
        'api_key': 'sk-bdd8af5a04744a6abb3a5e7a6ad96687'  # 请替换为您的真实API密钥
    }
}

# 服务器配置
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# 使用说明：
# 1. 将此文件复制为 config.py
# 2. 在 config.py 中填入您的真实API密钥
# 3. 确保 config.py 不被提交到git仓库（已通过.gitignore保护）
# 4. 对于生产环境，建议使用环境变量而不是硬编码的API密钥
