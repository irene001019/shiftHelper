from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse, HTMLResponse
from pathlib import Path

from parseSchedule import parse_schedule_pdf
from schedule_manager import ScheduleManager
from typing import Optional

router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/upload-pdf-form", response_class=HTMLResponse)
async def upload_pdf_form():
    return """
    <html>
        <head>
        <title>Upload Schedule PDF</title>
        <style>
            body { font-family: sans-serif; padding: 2em; }
        </style>
        </head>
        <body>
        <h2>Upload Schedule PDF</h2>
        <form method="POST" action="/upload-pdf" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf" required />
            <br><br>
            <button type="submit">Upload</button>
        </form>
        <p style="color:green;">After upload, return to Gmail Add-on to view your shifts.</p>
        </body>
    </html>
    """

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...),
                    year: Optional[int] = Query(None),
                    month: Optional[int] = Query(None)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse({"error": "Only PDF files are supported."}, status_code=400)

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 解析 PDF → overall_schedule
    overall_schedule = parse_schedule_pdf(str(file_path), year, month)
    manager = ScheduleManager(overall_schedule)

    # 儲存 JSON 給前端查詢用
    json_path = UPLOAD_DIR / "flat_schedule.json"
    manager.export_to_json(str(json_path))

    # 儲存 .ics 給日曆匯入用
    # ics_path = UPLOAD_DIR / "schedule.ics"
    # manager.export_to_ics(str(ics_path))

    # # 記錄目前使用的 PDF 檔名（optional）
    # latest_pdf_tracker = UPLOAD_DIR / "latest_pdf.txt"
    # with open(latest_pdf_tracker, "w") as f:
    #     f.write(file.filename)

    return{
        "message": "✅ PDF parsed successfully",
        "ics_url": "/schedule?download_ics=true",
        "available_people_url": "/people",
        "schedule_url": "/schedule"
        }
        
      
    
