import uuid
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# User 스키마


class UserBase(BaseModel):
    username: str
    tier: str
    primary_line: str
    secondary_line: str
    is_captain: bool
    base_price: int
    profile_image_path: Optional[str] = None
    current_team_uuid: Optional[str] = None


class UserCreate(UserBase):
    user_uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))


class User(UserBase):
    user_uuid: str

    class Config:
        orm_mode = True

# Team 스키마


class TeamBase(BaseModel):
    team_name: str
    captain_uuid: str
    budget: int


class TeamCreate(TeamBase):
    team_uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Team(TeamBase):
    team_uuid: str

    class Config:
        orm_mode = True

# TeamPlayer 스키마


class TeamPlayerBase(BaseModel):
    team_uuid: str
    player_uuid: str


class TeamPlayerCreate(TeamPlayerBase):
    pass


class TeamPlayer(TeamPlayerBase):
    team_player_id: int

    class Config:
        orm_mode = True

# Auction 스키마


class AuctionBase(BaseModel):
    team_uuid: str
    player_uuid: str
    bid_amount: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    auction_status: str


class AuctionCreate(AuctionBase):
    auction_room_name: str


class Auction(AuctionBase):
    auction_room_name: str

    class Config:
        orm_mode = True

# AuctionRecord 스키마


class AuctionRecordBase(BaseModel):
    auction_room_name: str
    bidder_uuid: str
    bid_amount: int
    timestamp: Optional[datetime] = None


class AuctionRecordCreate(AuctionRecordBase):
    pass


class AuctionRecord(AuctionRecordBase):
    record_id: int

    class Config:
        orm_mode = True
