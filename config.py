# 项目配置文件

import os

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
        'api_key': os.environ.get('DASH_SCOPE_API_KEY')
    }
}

# 服务器配置
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}
