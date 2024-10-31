from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
import uuid
import enum
from .DBconn import Base

# Enum 타입 정의
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

# Users 테이블
class Users(Base):
  __tablename__ = "users"

  user_uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  username = Column(String, unique=True, nullable=False)
  email = Column(String, unique=True, nullable=False)
  provider = Column(String)
  google_id = Column(String, unique=True)
  profile_image_url = Column(String)
  tier = Column(Enum(TierEnum), default=TierEnum.IRON)
  primary_line = Column(Enum(LineEnum), nullable=False)
  secondary_line = Column(Enum(LineEnum), nullable=False)
  is_captain = Column(Boolean, default=False)
  base_price = Column(Integer, default=0)
  current_team_uuid = Column(String, ForeignKey("teams.team_uuid"))

  def __repr__(self):
    return f"<User {self.username}>"

# Teams 테이블
class Teams(Base):
  __tablename__ = "teams"

  team_uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  team_name = Column(String, unique=True, nullable=False)
  captain_uuid = Column(String, ForeignKey("users.user_uuid"), nullable=False)
  budget = Column(Integer, default=1000)

# TeamPlayers 테이블
class TeamPlayers(Base):
  __tablename__ = "team_players"

  team_uuid = Column(String, ForeignKey("teams.team_uuid"), primary_key=True)
  player_uuid = Column(String, ForeignKey("users.user_uuid"), primary_key=True)

# Auctions 테이블
class Auctions(Base):
  __tablename__ = "auctions"

  auction_room_name = Column(String, primary_key=True)
  team_uuid = Column(String, ForeignKey("teams.team_uuid"), nullable=False)
  player_uuid = Column(String, ForeignKey("users.user_uuid"), nullable=False)
  bid_amount = Column(Integer, nullable=False)
  start_time = Column(DateTime)
  end_time = Column(DateTime)
  auction_status = Column(Enum(AuctionStatusEnum), nullable=False)

# AuctionRecords 테이블
class AuctionRecords(Base):
  __tablename__ = "auction_records"

  record_id = Column(Integer, primary_key=True, autoincrement=True)
  auction_room_name = Column(String, ForeignKey("auctions.auction_room_name"), nullable=False)
  bidder_uuid = Column(String, ForeignKey("users.user_uuid"), nullable=False)
  bid_amount = Column(Integer, nullable=False)
  timestamp = Column(DateTime)

# Tokens 테이블
class Tokens(Base):
  __tablename__ = "tokens"

  token_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  user_uuid = Column(String, ForeignKey("users.user_uuid", ondelete="CASCADE"), nullable=False)
  refresh_token = Column(String, unique=True)
  access_token = Column(String)
  id_token = Column(String)
  expires_at = Column(DateTime, nullable=False)
