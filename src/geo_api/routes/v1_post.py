import requests
from fastapi.responses import JSONResponse

from ..functions import add_user_to_database, get_full_user_information, \
    get_direction_from_response, check_response_geoson
from ..configuration import API_GEO_URL, DATABASE_NAME, LOGGER
from ..schemas import UserParameters
from fastapi import APIRouter

v1_router = APIRouter()


@v1_router.post(
    '/add_user',
    response_class=JSONResponse)
def add_user(user_parameter: UserParameters) -> JSONResponse:
    """
    Add a new user to database

    **:return:**
    """
    status_code = 200
    try:
        response = requests.get(API_GEO_URL.format(user_parameter.postal_code))

        if check_response_geoson(response):
            city = get_direction_from_response(
                response=response)

            full_user_parameters = get_full_user_information(
                user_parameter=user_parameter, city=city)

            _, msg = add_user_to_database(DATABASE_NAME, full_user_parameters)
            LOGGER.info(msg)
            message = msg
        else:
            message = f"The postal code {user_parameter.postal_code} doesn't exits"
            LOGGER.info(message)
    except Exception as e:
        message = "There was a problem. msg {}".format(e)
        status_code = 404
        LOGGER.error(message)

    return JSONResponse(
        content={
            "msg": message,
        },
        status_code=status_code,
    )
