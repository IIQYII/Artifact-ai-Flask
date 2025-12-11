import torch
import clip
from PIL import Image
import pandas as pd
from fastapi import FastAPI

# 测试PyTorch（GPU/CPU兼容）
print("PyTorch版本：", torch.__version__)
print("GPU支持：", torch.cuda.is_available())

# 测试CLIP模型加载（首次运行自动下载预训练模型）
model, preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")
print("CLIP模型加载成功")

# 测试其他依赖
print("Pillow、pandas、FastAPI导入成功")