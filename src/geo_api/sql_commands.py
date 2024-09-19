import sqlite3


def execute_sql_command(
        database: str, command: str):
    """
    Execute a command

    :param database: database name
    :param command:

    :return: get the result
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(command)
    conn.commit()
    return c.fetchall()


def define_commands_sql():
    """
    Define all commands used on the
    :return:
    """
    cmds = {
        'select.username':
            '''
            SELECT * FROM master WHERE user_name = '{}'
            ''',
        'select.max':
            '''
            SELECT
            max(id)
            FROM {} 
            ''',
        'select.postal_code':
            '''
            SELECT
            detail.id
            FROM detail 
            WHERE detail.postal_code = '{}'
            ''',
        'insert.master':
            '''
            INSERT INTO master (id, user_name)
            VALUES ({}, '{}')
            ''',
        'insert.relations':
            '''
            INSERT INTO relations (id, user_id, detail_id)
            VALUES ({}, {}, {})
            ''',
        'insert.details':
            '''
            INSERT INTO details (id, postal_code, city)
            VALUES ({}, '{}', '{}')
            ''',
        'create.master':
            '''
            CREATE TABLE IF NOT EXISTS master
            ([id] INTEGER PRIMARY KEY, [user_name] TEXT)
            ''',
        'create.details':
            '''
            CREATE TABLE IF NOT EXISTS details
            ([id] INTEGER PRIMARY KEY, [postal_code] TEXT, 
            [city] TEXT)
            ''',
        'create.relations':
            '''
            CREATE TABLE IF NOT EXISTS relations
            ([id] INTEGER PRIMARY KEY, [user_id] INTEGER, [detail_id] INTEGER)
            ''',
    }

    return cmds


SQL_COMMANDS = define_commands_sql()


def define_command_sql(key_cmd: str, *args):
    return SQL_COMMANDS[key_cmd].format(*args)



