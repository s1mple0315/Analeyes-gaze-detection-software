import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Dict

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class Session(BaseModel):
    user_id: str
    video_name: str
    duration: float
    gaze_data: List[Dict[str, float]]
    timestamp: str