# 古代文物对话器 - 后端服务

## 项目概述
这是一个Flask后端服务，为古代文物对话器提供API接口支持。项目采用模块化设计，便于团队分工合作。

## 项目结构
```
.
├── app.py              # 主应用文件
├── config.py           # 配置文件
├── requirements.txt    # 依赖文件
├── README.md          # 项目说明
├── api/               # API接口模块
│   ├── image_api.py   # 图像识别接口
│   └── artifact_ai_generator_api.py
│   └── artifact_api.py
├── static/            # 静态文件目录（前端使用）
└── templates/         # 模板文件目录（前端使用）
```

## 接口说明

### 1. 图像识别接口
- **端点**: `POST /api/image-recognition/`
- **功能**: 接收图片文件，返回文物识别结果
- **输入**: 图片文件（form-data格式，字段名：image）
- **输出**: JSON格式的识别结果

**响应示例**:
```json
{
    "success": true,
    "data": {
        "artifact_name": "商代青铜鼎",
        "rtifact_dynasty": "商代",
    }
}
```

### 2. ai文物讲述接口
- **端点**: `POST /api/artifact_api/`
- **功能**: 接收JSON对话请求，返回AI回复
- **输入**: 图像识别返回的JSON和API_key
- **输出**: str格式的对话响应

```

## 运行方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务
```bash
python app.py
```

### 3. 访问服务
- 服务地址: http://localhost:5000

## 配置说明
配置文件`config.py`包含：
- 前端路径配置（静态文件、模板目录）
- API接口配置（端点、方法、描述）
- 服务器运行配置

## 安全配置说明

### API密钥保护
为了保护您的API密钥不被泄露，项目已配置了以下安全措施：

1. **.gitignore文件** - 已配置保护敏感文件，包括：
   - `config.py` - 主配置文件（包含API密钥）
   - `.env` 文件 - 环境变量文件
   - 临时文件和缓存文件

2. **配置模板** - 提供了 `config_template.py` 文件：
   - 请复制此文件为 `config.py`
   - 在 `config.py` 中填入您的真实API密钥
   - 确保 `config.py` 不被提交到git仓库

### 配置步骤
1. 复制配置模板：
   ```bash
   cp config_template.py config.py
   ```

2. 编辑 `config.py` 文件，填入您的API密钥：
   ```python
   API_CONFIG = {
       'artifact_narration': {
           'api_key': 'your_actual_api_key_here'  # 替换为真实密钥
       }
   }
   ```

3. 验证配置是否生效：
   ```bash
   python app.py
   ```

### 最佳实践建议
- 对于生产环境，建议使用环境变量而不是硬编码API密钥
- 定期轮换API密钥以提高安全性
- 不要将包含真实API密钥的配置文件提交到版本控制

