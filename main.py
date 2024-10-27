from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 연결된 모든 클라이언트를 추적하기 위한 리스트
connected_clients = []

@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 새 클라이언트 연결 처리
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"Client connected: {websocket.client}")

    try:
        # 새 클라이언트에 환영 메시지 전송
        await websocket.send_text(f"Welcome client: {websocket.client}")

        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            logger.info(f"Message received: {data} from: {websocket.client}")

            # 모든 연결된 클라이언트에게 메시지 브로드캐스트
            disconnected_clients = []
            for client in connected_clients:
                try:
                    await client.send_text(f"Message from {websocket.client}: {data}")
                except Exception:
                    # 메시지 전송 실패 시, 연결이 끊긴 클라이언트로 간주
                    disconnected_clients.append(client)

            # 끊긴 클라이언트들을 연결된 클라이언트 리스트에서 제거
            for client in disconnected_clients:
                connected_clients.remove(client)

    except WebSocketDisconnect:
        # 클라이언트 연결 해제 시 처리
        logger.info(f"Client disconnected: {websocket.client}")
        connected_clients.remove(websocket)

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()
