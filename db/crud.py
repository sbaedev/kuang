from sqlalchemy.orm import Session
from .DBmodels import Users, Teams, TeamPlayers, Auctions, AuctionRecords
from .schemas import UserCreate, TeamCreate, TeamPlayerCreate, AuctionCreate, AuctionRecordCreate
from datetime import datetime, timezone

# User 생성


def create_user(db: Session, user: UserCreate):
    db_user = Users(
        user_uuid=user.user_uuid,
        username=user.username,
        tier=user.tier,
        primary_line=user.primary_line,
        secondary_line=user.secondary_line,
        is_captain=user.is_captain,
        base_price=user.base_price,
        profile_image_path=user.profile_image_path,
        current_team_uuid=user.current_team_uuid,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User 조회


def get_user(db: Session, user_uuid: str):
    return db.query(Users).filter(Users.user_uuid == user_uuid).first()

# User 목록 조회


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Users).offset(skip).limit(limit).all()

# User 업데이트


def update_user(db: Session, user_uuid: str, user: UserCreate):
    db_user = db.query(Users).filter(Users.user_uuid == user_uuid).first()
    if db_user:
        db_user.username = user.username
        db_user.tier = user.tier
        db_user.primary_line = user.primary_line
        db_user.secondary_line = user.secondary_line
        db_user.is_captain = user.is_captain
        db_user.base_price = user.base_price
        db_user.profile_image_path = user.profile_image_path
        db_user.current_team_uuid = user.current_team_uuid
        db.commit()
        db.refresh(db_user)
    return db_user

# User 삭제


def delete_user(db: Session, user_uuid: str):
    db_user = db.query(Users).filter(Users.user_uuid == user_uuid).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Team 생성


def create_team(db: Session, team: TeamCreate):
    db_team = Teams(
        team_uuid=team.team_uuid,
        team_name=team.team_name,
        captain_uuid=team.captain_uuid,
        budget=team.budget
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

# Team 조회


def get_team(db: Session, team_uuid: str):
    return db.query(Teams).filter(Teams.team_uuid == team_uuid).first()

# Team 업데이트


def update_team(db: Session, team_uuid: str, team: TeamCreate):
    db_team = db.query(Teams).filter(Teams.team_uuid == team_uuid).first()
    if db_team:
        db_team.team_name = team.team_name
        db_team.captain_uuid = team.captain_uuid
        db_team.budget = team.budget
        db.commit()
        db.refresh(db_team)
    return db_team

# Team 삭제


def delete_team(db: Session, team_uuid: str):
    db_team = db.query(Teams).filter(Teams.team_uuid == team_uuid).first()
    if db_team:
        db.delete(db_team)
        db.commit()
    return db_team

# TeamPlayer 추가


def add_player_to_team(db: Session, team_player: TeamPlayerCreate):
    db_team_player = TeamPlayers(
        team_uuid=team_player.team_uuid,
        player_uuid=team_player.player_uuid
    )
    db.add(db_team_player)
    db.commit()
    db.refresh(db_team_player)
    return db_team_player

# Auction 생성


def create_auction(db: Session, auction: AuctionCreate):
    db_auction = Auctions(
        auction_room_name=auction.auction_room_name,
        team_uuid=auction.team_uuid,
        player_uuid=auction.player_uuid,
        bid_amount=auction.bid_amount,
        start_time=auction.start_time or datetime.now(timezone.utc),
        end_time=auction.end_time,
        auction_status=auction.auction_status
    )
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

# Auction 조회


def get_auction(db: Session, auction_room_name: str):
    return db.query(Auctions).filter(Auctions.auction_room_name == auction_room_name).first()

# AuctionRecord 추가


def create_auction_record(db: Session, auction_record: AuctionRecordCreate):
    db_auction_record = AuctionRecords(
        auction_room_name=auction_record.auction_room_name,
        bidder_uuid=auction_record.bidder_uuid,
        bid_amount=auction_record.bid_amount,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(db_auction_record)
    db.commit()
    db.refresh(db_auction_record)
    return db_auction_record

# AuctionRecord 조회


def get_auction_record(db: Session, record_id: int):
    return db.query(AuctionRecords).filter(AuctionRecords.record_id == record_id).first()
