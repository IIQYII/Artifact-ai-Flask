// 文物对话器前端逻辑
document.getElementById('submit-image').addEventListener('click', async () => {
    // 获取所有需要的 DOM 元素
    const fileInput = document.getElementById('image-upload');
    const statusMessage = document.getElementById('status-message');
    const resultsSection = document.getElementById('results-section');
    const artifactInfoDetails = document.getElementById('artifact-info-details');
    const narrationOutput = document.getElementById('narration-output');
    const BASE_URL = 'http://8.134.131.114/';

    // 1. 检查文件是否已选择
    const file = fileInput.files[0];
    if (!file) {
        statusMessage.textContent = '❌ 请先选择一个图片文件。';
        // 统一使用后端定义的CSS类名
        statusMessage.className = 'mt-4 font-medium text-red-600'; 
        return;
    }

    // 重置状态和显示区域
    statusMessage.textContent = '⏳ 正在上传图片并识别...';
    // 统一使用后端定义的CSS类名
    statusMessage.className = 'mt-4 font-medium text-yellow-600'; 
    resultsSection.style.display = 'none';
    artifactInfoDetails.innerHTML = '';
    narrationOutput.textContent = '正在努力加载...';

    const formData = new FormData();
    formData.append('image', file);
    
    // API 端点配置 (来自 Flask 后端)
    const RECOGNITION_ENDPOINT = BASE_URL + '/api/image-recognition';
    const NARRATION_ENDPOINT = BASE_URL + '/api/artifact-narration';

    try {
        // --- 步骤 1: 调用图像识别接口 ---
        
        const recognitionResponse = await fetch(RECOGNITION_ENDPOINT, {
            method: 'POST',
            body: formData 
        });

        // 检查HTTP状态码
        if (!recognitionResponse.ok) {
            throw new Error(`图像识别服务错误: ${recognitionResponse.status}`);
        }

        const recognitionResult = await recognitionResponse.json();

        if (!recognitionResult.success) {
            throw new Error(recognitionResult.message || '图片识别失败。');
        }

        const artifactData = recognitionResult.data;
        
        // 格式化并显示 JSON 数据
        artifactInfoDetails.innerHTML = formatArtifactData(artifactData);
        
        statusMessage.textContent = '✅ 图片识别成功，正在生成文物讲解...';
        statusMessage.className = 'mt-4 font-medium text-green-600';


        // --- 步骤 2: 调用文物讲解生成接口 ---
        
        // 构造符合 artifact_api.py 要求的请求 JSON
        const narrationRequestBody = {
            // artifact_api.py 期望的字段名: name 和 dynasty
            name: artifactData.artifact_name, 
            dynasty: artifactData.era
        };
        
        const narrationResponse = await fetch(NARRATION_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(narrationRequestBody) // 传入修正后的 body
        });

        // 检查 HTTP 状态码
        if (!narrationResponse.ok) {
             throw new Error(`讲解生成服务错误: ${narrationResponse.status}`);
        }

        // 讲解接口返回的是 JSON, 需要解析
        const narrationResult = await narrationResponse.json(); 

        if (!narrationResult.success) {
            // 如果后端返回了错误信息，使用它
            const errorMessage = narrationResult.error || narrationResult.message || '讲解生成失败。';
            throw new Error(errorMessage);
        }
        
        // 从返回的 JSON 中提取讲解文案
        const narrationText = narrationResult.data.narration; 

        // 直接将内容显示到输出区域
        narrationOutput.innerText = narrationText;
        
        statusMessage.textContent = '🎉 文物讲解生成成功！';
        resultsSection.style.display = 'block';

    } catch (error) {
        statusMessage.textContent = '❌ 操作失败: ' + error.message;
        // 统一使用后端定义的CSS类名
        statusMessage.className = 'mt-4 font-medium text-red-600'; 
        narrationOutput.textContent = '未能获取讲解文案。请检查后端服务和 API 密钥。';
        console.error('API 交互错误:', error);
    }
});

/**
 * 辅助函数：将文物 JSON 数据转化为用户友好的 HTML 列表
 * @param {object} data - 图像识别返回的 JSON 对象
 * @returns {string} - 包含 HTML 元素的字符串
 */
function formatArtifactData(data) {
    let html = '';
    // 定义一个映射，将 JSON key 转换为中文描述
    const keyMap = {
        'artifact_name': '文物名称',
        'artifact_type': '类型',
        'confidence': '置信度',
        'description': '描述',
        'era': '年代',
        'image_path': '临时图片路径', // 添加 image_api.py 返回的路径字段
    };

    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            // 排除临时文件路径，不显示给用户
            if (key === 'image_path') continue; 
            
            // 获取中文名，如果没有则使用原始 key
            const label = keyMap[key] || key;
            let value = data[key];

            // 特殊处理置信度，格式化为百分比
            if (key === 'confidence' && typeof value === 'number') {
                 value = (value * 100).toFixed(2) + '%';
            }
            
            // 使用 div 代替 ul/li 以便更好地控制样式
            html += `<div class="flex justify-between border-b border-gray-200 py-1">
                        <span class="font-semibold text-gray-700">${label}:</span> 
                        <span class="text-right">${value}</span>
                     </div>`;
        }
    }
    // 添加一个默认的描述，以防数据为空
    if (html === '') {
        return '<p class="text-gray-500">未识别到文物关键信息。</p>';
    }
    return html;
}