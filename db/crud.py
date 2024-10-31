from sqlalchemy.orm import Session
from .DBmodels import Users, Teams
from .schemas import UserCreate, TeamCreate

# 유저 생성
def create_user(db: Session, user: UserCreate):
  db_user = Users(**user.model_dump())
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

# 팀 생성
def create_team(db: Session, team: TeamCreate):
  db_team = Teams(**team.model_dump())
  db.add(db_team)
  db.commit()
  db.refresh(db_team)
  return db_team
