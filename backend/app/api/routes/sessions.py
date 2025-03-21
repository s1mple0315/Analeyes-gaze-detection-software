from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import Session
from app.db.mongo import sessions_collection, fs
from app.api.deps import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_sessions(user_id: str = Depends(get_current_user)):
    sessions = []
    async for session in sessions_collection.find({"user_id": user_id}):
        session["_id"] = str(session["_id"])
        if "video_id" in session:
            session["video_id"] = str(session["video_id"])
        sessions.append(session)
    return sessions

@router.post("/store")
async def store_session(
    video_name: str = Form(...),
    duration: float = Form(...),
    gaze_data: str = Form(...),
    video: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    try:
        gaze_data_list = eval(gaze_data)
    except:
        raise HTTPException(status_code=400, detail="Invalid gaze data format")
    
    video_content = await video.read()
    video_id = await fs.upload_from_stream(video_name, video_content)
    
    session = {
        "user_id": user_id,
        "video_id": video_id,
        "video_name": video_name,
        "duration": duration,
        "gaze_data": gaze_data_list,
        "timestamp": datetime.now().isoformat()
    }
    
    result = await sessions_collection.insert_one(session)
    return {"session_id": str(result.inserted_id)}

@router.get("/video/{session_id}")
async def get_session_video(session_id: str, user_id: str = Depends(get_current_user)):
    session = await sessions_collection.find_one({"_id": session_id, "user_id": user_id})
    if not session or "video_id" not in session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    video_stream = await fs.open_download_stream(session["video_id"])
    return StreamingResponse(video_stream, media_type="video/mp4")