from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import relationship
import enum
from .DBconn import Base
from datetime import datetime, timezone


class TierEnum(str, enum.Enum):
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    EMERALD = "EMERALD"
    DIAMOND = "DIAMOND"
    MASTER = "MASTER"
    GRANDMASTER = "GRANDMASTER"
    CHALLENGER = "CHALLENGER"


class LineEnum(str, enum.Enum):
    TOP = "TOP"
    JUG = "JUG"
    MID = "MID"
    AD = "AD"
    SUP = "SUP"


class AuctionStatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"


class Users(Base):
    __tablename__ = "users"
    user_uuid = Column(TEXT, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    tier = Column(Enum(TierEnum), nullable=False)
    primary_line = Column(Enum(LineEnum), nullable=False)
    secondary_line = Column(Enum(LineEnum), nullable=False)
    is_captain = Column(Boolean, default=False)
    base_price = Column(Integer, default=0)
    profile_image_path = Column(String)
    current_team_uuid = Column(TEXT, ForeignKey("teams.team_uuid"))


class Teams(Base):
    __tablename__ = "teams"
    team_uuid = Column(TEXT, primary_key=True)
    team_name = Column(String, unique=True, nullable=False)
    captain_uuid = Column(TEXT, ForeignKey("users.user_uuid"), nullable=False)
    budget = Column(Integer, default=1000)


class TeamPlayers(Base):
    __tablename__ = "team_players"
    team_player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_uuid = Column(TEXT, ForeignKey("teams.team_uuid"))
    player_uuid = Column(TEXT, ForeignKey("users.user_uuid"))


class Auctions(Base):
    __tablename__ = "auctions"
    auction_room_name = Column(String, primary_key=True)
    team_uuid = Column(TEXT, ForeignKey("teams.team_uuid"), nullable=False)
    player_uuid = Column(TEXT, ForeignKey("users.user_uuid"), nullable=False)
    bid_amount = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.now(timezone.utc))
    end_time = Column(DateTime)
    auction_status = Column(Enum(AuctionStatusEnum), nullable=False)


class AuctionRecords(Base):
    __tablename__ = "auction_records"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    auction_room_name = Column(
        String, ForeignKey("auctions.auction_room_name"))
    bidder_uuid = Column(TEXT, ForeignKey("users.user_uuid"))
    bid_amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
