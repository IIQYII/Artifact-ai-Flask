from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from artifact_recognizer import ArtifactRecognizer
import pandas as pd  # 必须添加，否则无法识别pd
app = FastAPI(title="文物识别服务", version="1.0")

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化识别器
recognizer = ArtifactRecognizer()


@app.post("/recognize")
async def recognize_artifact(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        result = recognizer.recognize(image_bytes)

        # 清理结果中的nan值
        if "result" in result and isinstance(result["result"], list):
            for item in result["result"]:
                item["confidence"] = item.get("confidence", 0.0) if not pd.isna(item.get("confidence")) else 0.0

        return result
    except Exception as e:
        # 确保返回合法JSON
        return {"success": False, "error": str(e), "result": []}

if __name__ == "__main__":
    uvicorn.run("service:app", host="0.0.0.0", port=8000, reload=True)