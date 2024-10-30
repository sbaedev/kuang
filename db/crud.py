from sqlalchemy.orm import Session
from . import DBmodels, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = DBmodels.User(
        username=user.username,
        is_captain=user.is_captain,
        base_price=user.base_price
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = DBmodels.Team(
        captain_id=team.captain_id,
        team_name=team.team_name,
        budget=team.budget
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_user(db: Session, user_id: int):
    return db.query(DBmodels.User).filter(DBmodels.User.user_id == user_id).first()


def get_team(db: Session, team_id: int):
    return db.query(DBmodels.Team).filter(DBmodels.Team.team_id == team_id).first()
