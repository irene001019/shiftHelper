from fastapi import FastAPI
from routes import schedule
from shiftCalendar.back_end.routes import upload


app = FastAPI()
app.include_router(upload.router)
app.include_router(schedule.router)
# UPLOAD_DIR = Path(__file__).parent / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# # @app.get("/infor")
# # def get_infor():
# #     settings = get_settings()
# #     return {
# #         "app_name": settings.app_name,
# #         "author": settings.author,
# #         "app_mode": settings.app_mode,
# #         "port": settings.port,
# #         "reload": settings.reload,
# #         "database_url": settings.database_url
# #     }

# # @app.get("/")
# # def hello_world():
# #     return "Hello World"

# @app.post("/upload-pdf")
# async def upload_pdf(file: UploadFile = File(...)):
#     if not file.filename.endswith(".pdf"):
#         return JSONResponse({"error": "Only PDF files are supported."}, status_code=400)

#     file_path = UPLOAD_DIR / file.filename
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     # 解析 PDF → overall_schedule
#     overall_schedule = parse_schedule_pdf(str(file_path))

#     # 建立 manager
#     manager = ScheduleManager(overall_schedule)

#     # 產出 .ics 檔
#     ics_path = UPLOAD_DIR / "schedule.ics"
#     manager.export_to_ics(str(ics_path))

#     # 產出 JSON 檔
#     json_path = UPLOAD_DIR / "flat_schedule.json"
#     manager.export_to_json(str(json_path))

#     # 可選：回傳 JSON 班表
#     return {
#         "message": "✅ PDF processed successfully",
#         "schedule": manager.flat_schedule,
#         "ics_url": "/download-ics"
#     }

# @app.get("/download-ics")
# def download_ics():
#     ics_path = UPLOAD_DIR / "schedule.ics"
#     if ics_path.exists():
#         return FileResponse(ics_path, media_type="text/calendar", filename="schedule.ics")
#     return JSONResponse({"error": "No ICS file available."}, status_code=404)

# @app.get("/schedule")
# def get_schedule(name: str = Query(None)):
#     json_path = UPLOAD_DIR / "flat_schedule.json"
#     if not json_path.exists():
#         return JSONResponse({"error": "No parsed schedule available."}, status_code=404)

#     with open(json_path, "r", encoding="utf-8") as f:
#         flat_schedule = json.load(f)

#     if name:
#         return [entry for entry in flat_schedule if entry["name"] == name]

#     return flat_schedule
