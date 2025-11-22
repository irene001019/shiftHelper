
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("❌ Error: credentials.json not found. Please download it from Google Cloud Console.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        print(f"❌ Error building service: {e}")
        return None

def add_events_to_calendar(events):
    """
    Adds a list of events to the user's primary calendar.
    events: List of dicts with 'date', 'start_time', 'end_time', 'name', etc.
    """
    service = get_service()
    if not service:
        return False

    print(f"📅 Syncing {len(events)} events to Google Calendar...")
    
    count = 0
    for entry in events:
        date_str = entry.get("date")
        start_str = entry.get("start_time")
        end_str = entry.get("end_time")
        name = entry.get("name")
        
        if not date_str or not start_str or not end_str:
            continue

        # Construct datetime strings for Google API (RFC3339)
        # Assuming local time for simplicity, or we can add timezone
        # Format: "2023-11-01T09:00:00"
        start_dt = f"{date_str}T{start_str}:00"
        end_dt = f"{date_str}T{end_str}:00"
        
        # Format: "Work {close_duty}({duty})"
        # Examples: "Work 1(F)", "Work 2", "Work (F)", "Work"
        
        close_duty = entry.get('close_duty')
        duty = entry.get('duty')
        
        summary_parts = ["Work"]
        if close_duty:
            summary_parts.append(f" {close_duty}")
        if duty:
            summary_parts.append(f"({duty})")
            
        summary = "".join(summary_parts)
        description = f"Shift: {entry.get('duty', '')} {entry.get('close_duty', '')}"
        
        event_body = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_dt,
                'timeZone': 'America/Winnipeg', # Adjust as needed
            },
            'end': {
                'dateTime': end_dt,
                'timeZone': 'America/Winnipeg',
            },
        }

        try:
            service.events().insert(calendarId='primary', body=event_body).execute()
            print(f"✅ Added: {summary} on {date_str}")
            count += 1
        except Exception as e:
            print(f"⚠️ Failed to add event {summary}: {e}")

    print(f"🎉 Successfully added {count} events.")
    return True
