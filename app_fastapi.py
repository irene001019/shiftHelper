from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import os
from datetime import datetime
from utils.parseSchedule import parse_schedule_pdf
from utils.schedule_manager import ScheduleManager
from utils import google_calendar

app = FastAPI(title="ShiftHelper")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main index.html page"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/close-shift")
async def close_shift_redirect():
    """Redirect to main page (SPA handles tab switching)"""
    return RedirectResponse(url="/")


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    person_name: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    sync_google: Optional[str] = Form(None)
):
    """
    Handle PDF upload, parse schedule, generate ICS file, and optionally sync to Google Calendar
    """
    try:
        # Save uploaded PDF
        pdf_path = os.path.join("uploads", file.filename)
        with open(pdf_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Derive year/month from start_date if available, else use current date
        year, month = None, None
        if start_date:
            try:
                dt = datetime.strptime(start_date, "%Y-%m-%d")
                year = dt.year
                month = dt.month
            except ValueError:
                pass
        
        if not year or not month:
            now = datetime.now()
            year = now.year
            month = now.month
        
        sync_enabled = sync_google == "on"
        
        print(f"📄 Received {pdf_path} ({year}-{month} : {person_name}) Date Range: {start_date} to {end_date} Sync: {sync_enabled}")
        
        # Process the uploaded PDF
        parsed = parse_schedule_pdf(pdf_path, year, month)
        mgr = ScheduleManager(parsed)
        
        # Export to ICS and JSON
        ics_path = os.path.join("output", "schedule.ics")
        json_path = os.path.join("output", "schedule.json")
        mgr.export_to_ics(
            file_path=ics_path,
            filter_fn=lambda e: e.get("name") == person_name,
            start_date=start_date,
            end_date=end_date
        )
        mgr.export_to_json(
            file_path=json_path,
            filter_fn=lambda e: e.get("name") == person_name,
            start_date=start_date,
            end_date=end_date
        )
        
        # Handle Google Calendar sync
        sync_msg = ""
        if sync_enabled:
            all_events = mgr.flat_schedule
            filtered_events = [e for e in all_events if e.get("name") == person_name]
            if start_date:
                filtered_events = [e for e in filtered_events if e.get("date") and e.get("date") >= start_date]
            if end_date:
                filtered_events = [e for e in filtered_events if e.get("date") and e.get("date") <= end_date]
            
            success = google_calendar.add_events_to_calendar(filtered_events)
            if success:
                sync_msg = "<br><b>✅ Synced to Google Calendar!</b>"
            else:
                sync_msg = "<br><b>⚠️ Sync failed. Check console/credentials.</b>"
        
        # Return success HTML
        msg = f"""
        <html><body style='font-family:sans-serif; text-align:center;'>
        <h2>Successfully converted {os.path.basename(pdf_path)}!</h2>
        {sync_msg}
        <br><br><a href='/download/schedule.ics'>Download ICS file</a><br><br>
        <a href='/'>⬅ Back</a>
        </body></html>
        """
        return HTMLResponse(content=msg)
    
    except Exception as e:
        print(f"⚠️ Error processing upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated ICS files"""
    file_path = os.path.join("output", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="text/calendar",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
