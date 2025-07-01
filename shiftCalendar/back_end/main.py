from fastapi import FastAPI
from routes import schedule, upload
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(upload.router)
app.include_router(schedule.router)

import os
print("🧪 Current working dir:", os.getcwd())
print("📁 Available files:", os.listdir("."))


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")