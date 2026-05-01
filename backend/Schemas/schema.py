from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PredictionRequest(BaseModel):
    features: List[float]
    model_key: str = "Set-1"
