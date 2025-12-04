from flask import Blueprint, request, jsonify
from config import API_CONFIG
from .artifact_ai_generator import generate_artifact_story

# 创建文物讲解API蓝图
artifact_api = Blueprint('artifact_api', __name__)

@artifact_api.route('/', methods=['POST'])
def generate_narration():
    """
    文物讲解生成接口
    输入: JSON格式的文物信息
    输出: JSON格式的AI生成讲解文案
    
    接口说明:
    - 接收POST请求,包含文物信息的JSON数据
    - 返回AI生成的文物讲解文案
    - 不需要历史记录功能
    
    请求JSON格式示例:
    {
        "name": "兵马俑",
        "dynasty": "秦朝"
    }
    """
    try:
        # 检查请求数据
        if not request.is_json:
            return jsonify({
                'error': '请求必须是JSON格式',
                'code': 400
            }), 400
        
        data = request.get_json()
        
        # 验证必要字段
        if not data:
            return jsonify({
                'error': '请求数据不能为空',
                'code': 400
            }), 400
        
        name = data.get('name', '')
        dynasty = data.get('dynasty', '')
        
        # 检查必要参数
        if not name:
            return jsonify({
                'error': '缺少必要字段: name',
                'code': 400
            }), 400
        
        if not dynasty:
            return jsonify({
                'error': '缺少必要字段: dynasty',
                'code': 400
            }), 400
        
        # 获取API密钥
        api_key = API_CONFIG['artifact_narration'].get('api_key', '')
        if not api_key:
            return jsonify({
                'error': 'API密钥未配置',
                'code': 500
            }), 500
        
        # 调用AI生成函数
        narration = generate_artifact_story(name, dynasty, api_key)
        
        # 返回结果
        result = {
            'success': True,
            'message': '文物讲解生成成功',
            'data': {
                'name': name,
                'dynasty': dynasty,
                'narration': narration
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'生成文物讲解时发生错误: {str(e)}',
            'code': 500
        }), 500
