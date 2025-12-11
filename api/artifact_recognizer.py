import torch
import clip
from PIL import Image
import io
import pandas as pd
import os

class ArtifactRecognizer:
    def __init__(self):
        # 加载CLIP模型（自动适配GPU/CPU）
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        print(f"CLIP模型加载完成，运行设备：{self.device}")

        # 加载候选标签和文物数据
        self.candidate_labels = self._load_labels()
        
        # 获取数据文件路径（相对于当前文件位置）
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        artifact_data_path = os.path.join(data_dir, 'artifact_data.csv')
        self.artifact_df = pd.read_csv(artifact_data_path, encoding="utf-8")

        # 编码标签文本（提前计算，提升识别速度）
        self.encoded_labels = self._encode_labels()

    def _load_labels(self):
        """加载候选标签列表"""
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        labels_path = os.path.join(data_dir, 'candidate_labels.txt')
        with open(labels_path, "r", encoding="utf-8") as f:
            labels = [line.strip() for line in f if line.strip()]
        return labels

    def _encode_labels(self):
        """将标签文本编码为CLIP向量"""
        text = clip.tokenize(self.candidate_labels).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text)
        return text_features / text_features.norm(dim=-1, keepdim=True)  # 归一化

    def process_image(self, image_input):
        """图片预处理：支持文件路径或字节流输入"""
        try:
            if isinstance(image_input, bytes):
                img = Image.open(io.BytesIO(image_input)).convert("RGB")
            elif isinstance(image_input, str):
                img = Image.open(image_input).convert("RGB")
            else:
                return None

            # CLIP标准预处理： resize + center crop + 归一化
            processed = self.preprocess(img).unsqueeze(0).to(self.device)
            return processed
        except Exception as e:
            print(f"图片预处理失败：{str(e)}")
            return None

    def recognize(self, image_input, top_k=3, conf_threshold=0.2):
        """
        核心识别函数：返回Top K个文物匹配结果
        :param image_input: 图片路径（str）或字节流（bytes）
        :param top_k: 返回前K个结果
        :param conf_threshold: 置信度阈值（低于此值视为未识别）
        :return: 字典，包含识别结果或错误信息
        """
        try:
            # 图片预处理
            image_tensor = self.process_image(image_input)
            if image_tensor is None:
                return {"success": False, "error": "图片预处理失败"}

            # 图片编码
            with torch.no_grad():
                image_features = self.model.encode_image(image_tensor)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)

            # 计算相似度（余弦相似度）
            similarity = (100.0 * image_features @ self.encoded_labels.T).softmax(dim=-1)
            values, indices = similarity.topk(top_k)

            # 解析结果
            results = []
            for val, idx in zip(values[0], indices[0]):
                conf = round(val.item(), 3)
                # 过滤nan或低于阈值的置信度
                if pd.isna(conf) or conf < conf_threshold:
                    continue

                label = self.candidate_labels[idx]
                name, dynasty = label.split("-", 1) if "-" in label else ("未知", "未知")

                # 匹配文物介绍，处理空值
                match = self.artifact_df[
                    (self.artifact_df["name"].str.contains(name, na=False)) &
                    (self.artifact_df["dynasty"] == dynasty)
                    ]
                intro = match["intro"].values[0] if not match.empty and not pd.isna(
                    match["intro"].values[0]) else "暂无介绍"

                results.append({
                    "name": name,
                    "dynasty": dynasty,
                    "confidence": conf if not pd.isna(conf) else 0.0,  # 替换nan为0.0
                    "intro": intro
                })

            if not results:
                return {"success": False, "error": "未识别到已知文物，请上传清晰的文物图片"}
            return {"success": True, "result": results}
        except Exception as e:
            return {"success": False, "error": f"识别异常：{str(e)}", "result": []}

# 测试代码（可选）
if __name__ == "__main__":
    recognizer = ArtifactRecognizer()
    test_image = "./test_images/陶武士俑.jpg"  # 新建test_images文件夹，放入测试图片
    result = recognizer.recognize(test_image)
    print(result)
