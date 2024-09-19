from src.geo_api.functions import exist_user
from src.geo_api.sql_commands import execute_sql_command, define_command_sql
from src.geo_api.configuration import  DATABASE_NAME


def test_add_twice_users_db():
    """
    Add two users with the same name and same id
    :return:
    """
    command = define_command_sql(
        'insert.master', 123, 'USER_0001')
    execute_sql_command(DATABASE_NAME, command)

    try:
        command = define_command_sql(
            'insert.master', 123, 'USER_0002')
        execute_sql_command(DATABASE_NAME, command)
    except Exception as e:
        return True


def test_exist_user():
    state_no_exist = exist_user(DATABASE_NAME, 'USUARIO_QUE_NO_ESTA')
    state_exist = exist_user(DATABASE_NAME, 'USER_0001')
    return state_exist and not state_no_exist
