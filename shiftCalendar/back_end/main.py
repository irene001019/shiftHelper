from fastapi import FastAPI
from routes import schedule, upload, auth
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(upload.router)
app.include_router(schedule.router)
app.include_router(auth.router)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")