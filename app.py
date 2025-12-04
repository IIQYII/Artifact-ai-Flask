from flask import Flask, request, jsonify, render_template
from config import FRONTEND_CONFIG, API_CONFIG, SERVER_CONFIG
import os

# 创建Flask应用
app = Flask(__name__, 
        static_folder=FRONTEND_CONFIG['static_folder'],
        template_folder=FRONTEND_CONFIG['template_folder'])

# 导入API路由
from api.image_api import image_api
from api.artifact_api import artifact_api

# 注册API蓝图
app.register_blueprint(image_api, url_prefix=API_CONFIG['image_recognition']['endpoint'])
app.register_blueprint(artifact_api, url_prefix=API_CONFIG['artifact_narration']['endpoint'])

@app.route('/')
def index():
    """项目首页 - 提供JSON API测试页面"""
    return render_template('index.html')

@app.route('/api')
def api_info():
    """API信息页面，返回JSON格式的接口文档"""
    return jsonify({
        'message': '古代文物对话器后端服务',
        'apis': {
            'image_recognition': API_CONFIG['image_recognition'],
            'artifact_narration': API_CONFIG['artifact_narration']
        }
    })

if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs(FRONTEND_CONFIG['static_folder'], exist_ok=True)
    os.makedirs(FRONTEND_CONFIG['template_folder'], exist_ok=True)
    
    # 启动服务器
    app.run(
        host=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        debug=SERVER_CONFIG['debug']
    )
