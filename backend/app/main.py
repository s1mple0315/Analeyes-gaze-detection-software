from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.sessions import router as sessions_router
from app.db.mongo import init_db

app = FastAPI(
    title="Gaze Tracker API", description="API for Gaze Tracker", version="0.1"
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(sessions_router, prefix="/sessions", tags=["sessions"])


@app.on_event("startup")
async def startup_event():
    await init_db()
