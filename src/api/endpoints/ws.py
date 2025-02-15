from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.infrastructure.websocket.manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
