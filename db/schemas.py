from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
  username: str
  is_captain: bool
  base_price: int

class UserResponse(BaseModel):
  user_id: int
  username: str
  is_captain: bool
  base_price: int
  status: bool

  class Config:
    orm_mode = True

class TeamCreate(BaseModel):
  captain_id: int
  team_name: str
  budget: int

class TeamResponse(BaseModel):
  team_id: int
  captain_id: int
  team_name: str
  budget: int

  class Config:
    orm_mode = True
