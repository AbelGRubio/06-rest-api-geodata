from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..configuration import LOGGER
from ..functions import add_user, update_user
from ..models import ApiUser
from ..schemas import UserSchema, ShowUserSchema

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


@v1_router.get("/users/", response_model=list[ShowUserSchema])
def user_listing():
    users_ = ApiUser.select()
    return [ShowUserSchema.from_orm(usr_) for usr_ in users_]


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