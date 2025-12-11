from flask import Blueprint, request, jsonify
from config import FRONTEND_CONFIG
import os
from .artifact_recognizer import ArtifactRecognizer

# 创建图像识别API蓝图
image_api = Blueprint('image_api', __name__)

# 初始化图像识别器
recognizer = ArtifactRecognizer()

@image_api.route('/', methods=['POST'])
def image_recognition():
    """
    图像识别接口
    输入: 图片文件
    输出: JSON格式的识别结果
    
    接口说明:
    - 接收POST请求, 包含图片文件
    - 返回文物识别结果的JSON数据
    - 前端可以通过此接口上传文物图片进行识别
    """
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({
                'error': '未找到图片文件',
                'code': 400
            }), 400
        
        image_file = request.files['image']
        
        # 检查文件是否为空
        if image_file.filename == '':
            return jsonify({
                'error': '未选择文件',
                'code': 400
            }), 400
        
        # 检查文件格式
        if not allowed_file(image_file.filename):
            return jsonify({
                'error': f'不支持的文件格式，支持格式: {", ".join(FRONTEND_CONFIG["allowed_extensions"])}',
                'code': 400
            }), 400
        
        # 使用图像识别器处理图片
        image_bytes = image_file.read()
        recognition_result = recognizer.recognize(image_bytes)
        
        # 转换结果格式以匹配现有API结构
        if recognition_result.get('success'):
            # 成功识别到文物
            results = recognition_result['result']
            if results:
                # 返回最匹配的结果
                best_match = results[0]
                result = {
                    'success': True,
                    'message': '图像识别成功',
                    'data': {
                        'artifact_type': '文物',  # 文物类型
                        'artifact_name': best_match['name'],  # 文物名称
                        'era': best_match['dynasty'],  # 年代
                        'description': best_match['intro'],  # 描述
                        'confidence': best_match['confidence'],  # 识别置信度
                    },
                    'all_results': results  # 包含所有匹配结果
                }
            else:
                result = {
                    'success': False,
                    'error': '未识别到已知文物',
                    'code': 404
                }
        else:
            # 识别失败
            result = {
                'success': False,
                'error': recognition_result.get('error', '识别失败'),
                'code': 500
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'处理图像时发生错误: {str(e)}',
            'code': 500
        }), 500

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in FRONTEND_CONFIG['allowed_extensions']

# 清理临时文件的函数（可选）
@image_api.route('/cleanup', methods=['POST'])
def cleanup_temp_files():
    """清理临时文件接口"""
    try:
        # TODO: 实现临时文件清理逻辑
        return jsonify({'message': '清理完成'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
