from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..configuration import MANAGER
from ..gpt_connection import chat_with_gpt
from ..models import Message
from ..schemas import MessageSchema

ws_router = APIRouter()


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await MANAGER.connect(client_id, websocket)
    msg_ = MessageSchema(user_id=client_id)
    msg_.connection_msg()
    await MANAGER.broadcast(msg_.to_json())
    try:
        while True:
            data = await websocket.receive_text()
            message_data = MessageSchema.parse_raw(data)
            msg = Message.create(user_id=message_data.user_id,
                                 content=message_data.content)
            await MANAGER.broadcast(message_data.to_json())
    except WebSocketDisconnect:
        MANAGER.disconnect(client_id)
        msg_ = MessageSchema(user_id=client_id)
        msg_.disconnection_msg()
        await MANAGER.broadcast(msg_.to_json())


@ws_router.websocket("/gpt/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await MANAGER.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            gpt_name = f'gpt-client-{client_id}'
            msg = Message.create(user_id=client_id, content=data)
            gpt_response = chat_with_gpt(msg.content)
            # await MANAGER.send_personal_message(f"You wrote: {data}", websocket)
            msg_gpt = Message.create(user_id=gpt_name, content=gpt_response)
            msg_ = MessageSchema(user_id=gpt_name,
                                 content=gpt_response,
                                 timestamp=msg_gpt.timestamp)
            await MANAGER.broadcast(msg_.to_json())
    except WebSocketDisconnect:
        MANAGER.disconnect(client_id)
        msg_ = MessageSchema(user_id=client_id)
        msg_.disconnection_msg()
        await MANAGER.broadcast(msg_.to_json())


@ws_router.websocket("/ws/signal/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await MANAGER.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await MANAGER.broadcast(data)
    except WebSocketDisconnect:
        MANAGER.disconnect(client_id)


@ws_router.get("/connected_users")
async def get_connected_users():
    users = MANAGER.get_connected_users()
    return {"connected_users": users}
