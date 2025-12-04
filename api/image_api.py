from flask import Blueprint, request, jsonify
from config import FRONTEND_CONFIG
import os

# 创建图像识别API蓝图
image_api = Blueprint('image_api', __name__)

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
        
        # TODO: 这里需要集成图像识别模块
        # 示例处理流程：
        # 1. 保存上传的图片到临时目录
        # 2. 调用图像识别算法处理图片
        # 3. 返回识别结果
        
        # 临时保存文件（示例）
        filename = f"temp_{os.urandom(8).hex()}.jpg"
        temp_path = os.path.join('temp', filename)
        os.makedirs('temp', exist_ok=True)
        image_file.save(temp_path)
        
        # 返回数据格式的示例(当然只是临时的，具体还要看怎么实现的xd)
        result = {
            'success': True,
            'message': '图像识别成功',
            'data': {
                'artifact_type': '青铜器',  # 文物类型
                'artifact_name': '青铜鼎',  # 文物名称
                'era': '商代',  # 年代
                'description': '这是一件商代青铜鼎，具有重要的历史价值...',  # 描述
                'confidence': 0.37,  # 识别置信度
            },
            'image_path': temp_path  # 临时文件路径（实际使用时可能需要删除）
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
