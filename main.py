from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger
from typing import Dict, List, Annotated
from sqlalchemy.orm import Session
from db import crud, schemas
from db.DBconn import SessionLocal, engine
from db.DBmodels import Base

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 데이터베이스 세션 의존성


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용자 생성 엔드포인트


@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# 팀 생성 엔드포인트


@app.post("/teams/", response_model=schemas.TeamResponse)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)

# 특정 사용자 조회 엔드포인트


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 특정 팀 조회 엔드포인트


@app.get("/teams/{team_id}", response_model=schemas.TeamResponse)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db=db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=["*"],  # 필요에 따라 조정
#   allow_credentials=True,
#   allow_methods=["*"],
#   allow_headers=["*"],
# )


templates = Jinja2Templates(directory="templates")

# 방별로 클라이언트를 추적하기 위한 딕셔너리
rooms: Dict[str, Dict[str, WebSocket]] = {}


@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, client_id: str):
    # 새 클라이언트 연결 처리
    await websocket.accept()
    # 중복 접속 확인 (client_id를 기준으로)
    if room_name not in rooms:
        rooms[room_name] = {}
    # 중복 접속 방지: 이미 같은 client_id가 있는지 확인
    if client_id in rooms[room_name]:
        await websocket.send_text("You are already connected to this room.")
        await websocket.close()
        return

    # 방에 클라이언트 추가
    rooms[room_name][client_id] = websocket
    logger.info(f"Client connected: {client_id} in room: {room_name}")
    print(f"rooms value\n{rooms}")
    try:
        # 새 클라이언트에 환영 메시지 전송
        await websocket.send_text(f"Welcome client: {client_id}")
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            logger.info(f"Message received: {data} from: {client_id}")
            # 모든 연결된 클라이언트에게 메시지 브로드캐스트
            disconnected_clients = []
            for client_key, client in rooms[room_name].items():
                try:
                    await client.send_text(f"Message from {client_id}: {data}")
                except Exception:
                    # 메시지 전송 실패 시, 연결이 끊긴 클라이언트로 간주
                    disconnected_clients.append(client_key)
            # 끊긴 클라이언트들을 방에서 제거
            for client_key in disconnected_clients:
                del rooms[room_name][client_key]
    except WebSocketDisconnect:
        # 클라이언트 연결 해제 시 처리
        logger.info(f"Client disconnected: {client_id}")
        if client_id in rooms[room_name]:
            del rooms[room_name][client_id]
        # 방에 클라이언트가 더 이상 없으면 방 삭제
        if not rooms[room_name]:
            del rooms[room_name]


def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()
