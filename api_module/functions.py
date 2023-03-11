import os

import requests
from dotenv import load_dotenv

from .logger_api import LOGGER
from .schemas import UserFullParameters, UserParameters
from .sql_commands import execute_sql_command, define_command_sql

load_dotenv()

EXIST_USER_MSG = os.getenv("EXIST_USER_MSG")
ADDED_USER_MSG = os.getenv("ADDED_USER_MSG")


def check_all_vars(vtc: list) -> bool:
    """
    vtc variables to check
    Check if all variables exits on the .env file.

    :param vtc: variable names to check if exits on the environment.
    :type vtc: list

    :return: false if any variable doesn't exist on the environment, true otherwise.
    """
    for var_name in vtc:
        if var_name not in os.environ.keys():
            return False
    return True


def check_response_geoson(response: requests):
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
        placename = response.json()['postalCodes'][0]['placeName']
        adminname = response.json()['postalCodes'][0]['adminName1']
        country = response.json()['postalCodes'][0]['countryCode']
        return ', '.join([placename, adminname, country]) if full_dir else placename
    except Exception as e:
        LOGGER.error(f'Error getting information from request. Msg {e}')
        return ' '


def get_full_user_information(
        user_parameter: UserParameters, city: str) -> UserFullParameters:
    """
    Complete the information to save on the database.

    :param user_parameter: previous schema without city value
    :type user_parameter: UserParameters
    :param city: city name
    :type city: str

    :return: a schema with all information to include on the database
    :type :return: UserFullParameters
    """
    full_user_parameters = UserFullParameters()
    full_user_parameters.postal_code = user_parameter.postal_code
    full_user_parameters.user = user_parameter.user
    full_user_parameters.city = city
    return full_user_parameters


def get_max_key_database(database: str, table: str) -> (bool, str, int):
    """
    Get the max primary key of a table,
        * if the table is empty will get value of 0
        * Any error return value of -1
        * Otherwise return the value

    :param database: database name
    :type database: str
    :param table: table name
    :type table: str

    :return: boolean True it everything was ok, false other case.
             str message for the logger.
             int value of index.
    :type :return: (bool, str, int):
    """
    msg = 'Getting the max id for {}'.format(table)
    state = True
    try:
        command = define_command_sql('select.max', table)
        result = execute_sql_command(database, command)
        value = result[0][0]
        if value is None:
            value = 0
    except Exception as e:
        msg = 'Error getting the index. Msg: {}'.format(e)
        state = False
        value = -1

    if state:
        LOGGER.debug(msg)
    else:
        LOGGER.error(msg)

    return state, msg, value


def get_id_postal_code(database: str, postal_code: str) -> (bool, str, int):
    """
    get the id for the postal code.

    :param database: database name
    :type database: str
    :param postal_code:
    :type postal_code: str

    :return: boolean True it everything was ok, false other case.
             str message for the logger.
             int value of index.
    :type :return: (bool, str, int):
    """
    msg = 'Getting the id for postal code {}'.format(postal_code)

    try:
        command = define_command_sql('select.postal_code', postal_code)
        result = execute_sql_command(database, command)
        value = result[0][0]
        state = True
    except Exception as e:
        _, msg, value = get_max_key_database(database, 'details')
        state = False

    return state, msg, value


def exist_user(
        database: str, username: str):
    """
    Check if the user is already on the database

    :param database:
    :param username:

    :return: True if the user already exist on the database, false otherwise
    """
    command = define_command_sql('select.username', username)
    result = execute_sql_command(database, command)
    exist = len(result) > 0
    return exist


def add_user_to_database(
        database: str,
        new_user: UserFullParameters) -> (bool, str):
    """
    Try to add a new user to the database. After all check if
    already exist the user.

    :param database:
    :param new_user:

    :return: a boolean if everything was ok.
    """
    the_user_exist = exist_user(database, new_user.user)

    msg = EXIST_USER_MSG
    state = True

    if not the_user_exist:
        *_, max_id_master = get_max_key_database(database, 'master')
        id_master = max_id_master + 1

        *_, max_id_relations = get_max_key_database(database, 'relations')
        id_relations = max_id_relations + 1

        state_details, _, value = get_id_postal_code(database, new_user.postal_code)

        id_details = value if state_details else value + 1

        try:
            command = define_command_sql(
                'insert.master', id_master, new_user.user)
            execute_sql_command(database, command)

            command = define_command_sql(
                'insert.relations', id_relations, id_master, id_details)
            execute_sql_command(database, command)

            if not state_details:
                command = define_command_sql(
                    'insert.details', id_details, new_user.postal_code, new_user.city)
                execute_sql_command(database, command)

            msg = ADDED_USER_MSG
            state = True

        except Exception as e:
            state = False
            msg = e

    if state:
        LOGGER.debug(msg)
    else:
        LOGGER.error(msg)

    return state, msg


def create_database(database: str) -> None:
    """
    Create a defined database with a specific name

    :param database: database name
    :type database: str

    :return: Nothing
    """
    state = True
    message = 'Database created!'

    try:
        command = define_command_sql(
            'create.master')
        execute_sql_command(database, command)

        command = define_command_sql(
            'create.relations')
        execute_sql_command(database, command)

        command = define_command_sql(
            'create.details')
        execute_sql_command(database, command)

    except Exception as e:
        message = "Error creating database. msg {}".format(e)
        state = False

    if state:
        LOGGER.info(message)
    else:
        LOGGER.error(message)

    return None


def check_exist_database(database: str) -> None:
    """
    Check if the database exist, otherwise the database will be created

    :param database: database name
    :type database: str

    :return:  Nothing
    """
    msg = 'Already exist the database!'

    if not os.path.exists(database):
        create_database(database)
    else:
        LOGGER.info(msg)

    return None
