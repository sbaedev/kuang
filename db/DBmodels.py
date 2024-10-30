from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .DBconn import Base

class User(Base):
  __tablename__ = "Users"

  user_id = Column(Integer, primary_key=True, index=True)
  username = Column(String, nullable=False)
  is_captain = Column(Boolean, nullable=False)
  base_price = Column(Integer)
  status = Column(Boolean, default=True)


class Team(Base):
  __tablename__ = "Teams"

  team_id = Column(Integer, primary_key=True, index=True)
  captain_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
  team_name = Column(String, nullable=False)
  budget = Column(Integer, CheckConstraint("budget >= 0"), nullable=False)


class TeamPlayer(Base):
  __tablename__ = "TeamPlayers"

  team_id = Column(Integer, ForeignKey("Teams.team_id"), primary_key=True)
  player_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)


class Auction(Base):
  __tablename__ = "Auctions"

  auction_id = Column(Integer, primary_key=True, index=True)
  team_id = Column(Integer, ForeignKey("Teams.team_id"), nullable=False)
  player_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
  bid_amount = Column(Integer, nullable=False)
  timestamp = Column(DateTime, default=datetime.utcnow)
  auction_status = Column(String, CheckConstraint("auction_status IN ('OPEN', 'CLOSED', 'IN_PROGRESS')"), default="OPEN")


class FinalTeamStat(Base):
  __tablename__ = "FinalTeamStats"

  team_id = Column(Integer, ForeignKey("Teams.team_id"), primary_key=True)
  player_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
  remaining_budget = Column(Integer, CheckConstraint("remaining_budget >= 0"), nullable=False)
