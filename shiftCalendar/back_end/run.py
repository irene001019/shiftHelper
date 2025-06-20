from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開發時自動重載
        workers=1     # 可依需要增加
    )