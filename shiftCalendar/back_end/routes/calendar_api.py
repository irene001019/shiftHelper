from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from pathlib import Path
import os, json

UPLOAD_DIR = Path(__file__).parent / "uploads"
LATEST_JSON = UPLOAD_DIR / "flat_schedule.json"

GOOGLE_CLIENT_CONFIG = {
    "web": {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["https://shifthelper.onrender.com/oauth2callback"]
    }
}

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # for local testing only

def create_flow():
    return Flow.from_client_config(
        GOOGLE_CLIENT_CONFIG,
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="https://shifthelper.onrender.com/oauth2callback"
    )

def create_calendar_events(credentials, user_name):
    if not LATEST_JSON.exists():
        return {"error": "No schedule data"}

    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    user_shifts = [entry for entry in schedule if entry.get("name") == user_name]
    service = build("calendar", "v3", credentials=credentials)

    for shift in user_shifts:
        event = {
            "summary": f"Shift: {shift.get('name')}",
            "start": {
                "dateTime": f"{shift['date']}T{shift['start_time']}:00",
                "timeZone": "America/Toronto"  # adjust as needed
            },
            "end": {
                "dateTime": f"{shift['date']}T{shift['end_time']}:00",
                "timeZone": "America/Toronto"
            }
        }
        service.events().insert(calendarId="primary", body=event).execute()

    return {"status": "✅ Events added"}
