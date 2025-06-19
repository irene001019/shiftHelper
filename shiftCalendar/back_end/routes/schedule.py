from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from typing import Optional
import json

from schedule_manager import ScheduleManager

router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
LATEST_JSON = UPLOAD_DIR / "flat_schedule.json"
LATEST_PDF_TRACKER = UPLOAD_DIR / "latest_pdf.txt"

@router.get("/schedule")
def get_schedule(
    name: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    week: Optional[int] = Query(None),
    download_ics: Optional[bool] = Query(False)
):
    """
    回傳已處理過的班表（從 flat_schedule.json 讀取）
    支援條件篩選（name, date, week），可選擇匯出 .ics
    """
    if not LATEST_JSON.exists():
        return JSONResponse({"error": "No parsed schedule available."}, status_code=404)

    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtered = [entry for entry in data if
                (not name or entry.get("name") == name) and
                (not date or entry.get("date") == date) and
                (not week or entry.get("week") == week)]

    if download_ics:
        manager = ScheduleManager([])
        manager.flat_schedule = filtered
        filename = f"{name or 'filtered'}_schedule.ics"
        ics_path = UPLOAD_DIR / filename
        manager.export_to_ics(str(ics_path))
        return FileResponse(
            path=ics_path,
            media_type="text/calendar",
            filename=filename
        )

    return {
        "success": True,
        "count": len(filtered),
        "data": filtered
    }

@router.get("/people")
def get_people():
    if not LATEST_JSON.exists():
        return JSONResponse({"error": "No parsed schedule available."}, status_code=404)

    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    names = sorted(set(entry["name"] for entry in data if "name" in entry))
    return {
        "success": True,
        "count": len(names),
        "names": names
    }
