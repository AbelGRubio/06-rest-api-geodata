import requests

from .configuration import LOGGER, API_GEO_URL
from .models import ApiUser
from .schemas import UserSchema


def check_response_geojson(response: requests):
    return len(response.json()['postalCodes']) > 0


def get_direction_from_response(
        response: requests, full_dir: bool = False) -> str:
    """
    Get the direction in string format.

    :param response: from the url request
    :type response: request
    :param full_dir: Boolean to indicate if
    :type full_dir: bool

    :return:
    :type :return: str
    """
    try:
        postal_codes_ = response.json()['postalCodes'][0]
        place_ = postal_codes_['placeName']
        admin_ = postal_codes_['adminName1']
        country = postal_codes_['countryCode']
        return ', '.join([place_, admin_, country]) \
            if full_dir else place_
    except Exception as e:
        LOGGER.error(f'Error getting information from request. Msg {e}')
        return ' '


def add_user(user_: UserSchema) -> str:
    """
    This function adds a user to the database. It first checks if the user's
    city is unknown and attempts to fetch it using an external API.
    If the user does not already exist in the database,
    it creates a new user entry; otherwise, it returns a message
    indicating the user already exists.

    :param user_: An instance of UserSchema containing user details such as
        name, postal_code, and city.

    :return: A string message indicating whether the user was added to the
        database or already exists.
    """
    message = "Added user {}:{} to database."

    if user_.city == '-':
        response = requests.get(API_GEO_URL.format(user_.postal_code))

        if check_response_geojson(response):
            user_.city = get_direction_from_response(
                response=response)

    exist_user = ApiUser.get_or_none(**user_.dict())

    if not exist_user:
        new_user = ApiUser.create(**user_.dict())
        message = message.format(new_user.id, new_user.name)
    else:
        message = 'The user already exists!'

    return message


def update_user(user_: ApiUser, user_update: UserSchema) -> ApiUser:
    """
    This function updates an existing ApiUser instance with new data provided
    in a UserSchema instance and returns the updated ApiUser

    :param user_: An instance of ApiUser representing the user to be updated.
    :param user_update:  An instance of UserSchema containing the new data
        for the user.

    :return: An updated ApiUser instance with the new data applied.
    """
    user_dict_ = user_update.dict(exclude_unset=True)

    user_.update(**user_dict_).where(ApiUser.id == user_.id).execute()

    user_updated = ApiUser.get(ApiUser.id == user_.id)

    return user_updated
