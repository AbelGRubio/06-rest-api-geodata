from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..configuration import MANAGER

ws_router = APIRouter()


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await MANAGER.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await MANAGER.send_personal_message(f"You wrote: {data}", websocket)
            await MANAGER.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        MANAGER.disconnect(websocket)
        await MANAGER.broadcast(f"Client #{client_id} left the chat")