from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Users 스키마
class UserBase(BaseModel):
  username: str
  email: str
  provider: Optional[str] = None
  google_id: Optional[str] = None
  profile_image_url: Optional[str] = None

class UserCreate(UserBase):
  primary_line: str
  secondary_line: str
  base_price: int = 0

class UserResponse(UserBase):
  user_uuid: uuid.UUID

# Team 스키마
class TeamBase(BaseModel):
  team_name: str

class TeamCreate(TeamBase):
  captain_uuid: str
  budget: int = 1000

class TeamResponse(TeamBase):
  team_uuid: uuid.UUID

# Token 스키마
class TokenBase(BaseModel):
  access_token: str
  refresh_token: Optional[str] = None
  expires_at: datetime
