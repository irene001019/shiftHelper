from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import os

from parseSchedule import parse_schedule_pdf
from schedule_manager import ScheduleManager

router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse({"error": "Only PDF files are supported."}, status_code=400)

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 解析 PDF → overall_schedule
    overall_schedule = parse_schedule_pdf(str(file_path))
    manager = ScheduleManager(overall_schedule)

    # 儲存 JSON 給前端查詢用
    json_path = UPLOAD_DIR / "flat_schedule.json"
    manager.export_to_json(str(json_path))

    # 儲存 .ics 給日曆匯入用
    ics_path = UPLOAD_DIR / "schedule.ics"
    manager.export_to_ics(str(ics_path))

    # # 記錄目前使用的 PDF 檔名（optional）
    # latest_pdf_tracker = UPLOAD_DIR / "latest_pdf.txt"
    # with open(latest_pdf_tracker, "w") as f:
    #     f.write(file.filename)

    return {
        "message": "✅ PDF parsed successfully",
        "ics_url": "/schedule?download_ics=true",
        "available_people_url": "/people",
        "schedule_url": "/schedule"
    }
