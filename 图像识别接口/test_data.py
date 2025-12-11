import pandas as pd

# 读取数据（处理中文乱码）
data_path = "./data/artifact_data.csv"
try:
    df = pd.read_csv(data_path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(data_path, encoding="gbk")  # Windows系统备选编码

# 数据清洗：过滤空值、去重
df = df.dropna(subset=["name", "dynasty"]).drop_duplicates(subset=["name", "dynasty"])

# 验证输出
print(f"有效文物数据条数：{len(df)}")
print("前5条数据：")
print(df[["name", "dynasty"]].head())

# 保存清洗后的数据（避免重复处理）
df.to_csv("./data/cleaned_artifact_data.csv", index=False, encoding="utf-8")
print("清洗后的数据已保存至 cleaned_artifact_data.csv")