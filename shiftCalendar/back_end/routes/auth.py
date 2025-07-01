from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from calendar_api import create_flow, create_calendar_events

router = APIRouter()

@router.get("/authorize-calendar")
async def authorize_calendar(name: str):
    flow = create_flow()
    auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    # Store state + name in session or database (simplified here as file)
    Path("uploads/state.json").write_text(json.dumps({"state": state, "name": name}))
    return RedirectResponse(auth_url)

@router.get("/oauth2callback")
async def oauth2callback(request: Request):
    state_file = Path("uploads/state.json")
    if not state_file.exists():
        return JSONResponse({"error": "Missing state."})

    data = json.loads(state_file.read_text())
    flow = create_flow()
    flow.fetch_token(code=request.query_params["code"])

    credentials = flow.credentials
    result = create_calendar_events(credentials, data["name"])
    return JSONResponse(result)
