import asyncio
from typing import List

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from ..configuration import LOGGER, MANAGER
from ..functions import add_user, update_user, save_file
from ..models import ApiUser, Message
from ..schemas import UserSchema, ShowUserSchema, MessageSchema

v1_router = APIRouter()


@v1_router.post(
    '/user',
    response_class=JSONResponse)
def adding_user(user_parameter: UserSchema) -> JSONResponse:
    """
    This function attempts to add a new user to the database. It handles
    exceptions and logs errors if they occur, returning a JSON
    response with a message and appropriate status code.

    :param user_parameter: An instance of UserSchema containing user details.

    :return A JSONResponse containing a message about the operation's success
        or failure and the corresponding status code.
    """
    status_code = 200

    try:
        message = add_user(user_parameter)
    except Exception as e:
        message = "There was a problem. msg {}".format(e)
        status_code = 404
        LOGGER.error(message)

    return JSONResponse(
        content={"msg": message},
        status_code=status_code,
    )


@v1_router.post("/upload-files/")
async def upload_files(files: List[UploadFile] = File(...)):
    tasks = [save_file(file) for file in files]
    results = await asyncio.gather(*tasks)
    return {"uploaded_files": results}


@v1_router.get("/connected_users")
async def get_connected_users():
    users = MANAGER.get_connected_users()
    return {"connected_users": users}


@v1_router.get("/users/", response_model=list[ShowUserSchema])
def user_listing():
    users_ = ApiUser.select()
    return [ShowUserSchema.from_orm(usr_) for usr_ in users_]


@v1_router.get("/messages")
def get_messages() -> List[MessageSchema]:
    messages = Message.select().order_by(Message.id.desc()).limit(10)
    return [MessageSchema.from_orm(msg) for msg in messages[::-1]]


@v1_router.put("/users/{user_id}", response_model=UserSchema)
def updating_user(user_id: str, user_update: UserSchema):
    """

    :param user_id:
    :param user_update:
    :return:
    """
    user_ = ApiUser.get_or_none(ApiUser.id == user_id)
    if not user_:
        return JSONResponse(status_code=404, content="User not found")

    user_updated = update_user(user_, user_update)

    return UserSchema.from_orm(user_updated)


@v1_router.delete("/users/{user_id}")
def delete_user(user_id: int):
    user_ = ApiUser.get_or_none(ApiUser.id == user_id)

    if not user_:
        return JSONResponse(status_code=404, content="User not found")

    user_.delete_instance()
    return JSONResponse(status_code=200, content="User deleted")


@v1_router.delete("/messages")
def delete_messages():
    Message.delete().execute()
    return JSONResponse(status_code=200, content="Messages deleted")


