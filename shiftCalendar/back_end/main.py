from fastapi import FastAPI
from routes import schedule, upload

app = FastAPI()
app.include_router(upload.router)
app.include_router(schedule.router)