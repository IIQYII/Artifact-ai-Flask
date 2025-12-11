import pandas as pd
import os

# 读取文物数据
data_path = "./data/artifact_data.csv"
df = pd.read_csv(data_path, encoding="utf-8")

# 生成候选标签（格式："文物名称-朝代"）
df = df.dropna(subset=["name", "dynasty"])  # 过滤空值
candidate_labels = [f"{row['name']}-{row['dynasty']}" for _, row in df.iterrows()]

# 去重并保存
candidate_labels = list(set(candidate_labels))
with open("./data/candidate_labels.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(candidate_labels))

print(f"生成候选标签共 {len(candidate_labels)} 条，已保存至 data/candidate_labels.txt")