import sqlite3 as sql
import os


DB_ROUTE = "D:\\PyCharm\\Projects\\TotalBotWar\\Database\\game_states.db"


def create_db():
    conn, cursor = get_connection()
    conn.close()


def create_table():
    conn, cursor = get_connection()
    cursor.execute(
        """CREATE TABLE game_states (
            ids text,
            teams text,
            healths text,
            types text,
            states text,
            positions text,
            directions text
        )
        """
    )
    conn.commit()
    conn.close()


def get_connection(db=DB_ROUTE):
    conn = sql.connect(db)
    cursor = conn.cursor()
    return conn, cursor


def insert_row(ids, teams, healths, types, states, positions, directions):
    print(f"ids : {ids}\nteams : {teams}\nhealths : {healths}\ntypes : {types}\nstates : {states}\npositions : {positions}\ndirections : {directions}\n")
    conn, cursor = get_connection()
    instruction = f"INSERT INTO game_states VALUES ('{ids}', '{teams}', '{healths}', '{types}', '{states}', '{positions}', '{directions}')"
    cursor.execute(instruction)
    conn.commit()
    conn.close()


def insert_many(data):
    conn, cursor = get_connection()
    cursor.executemany("""INSERT INTO game_states VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
    conn.commit()
    conn.close()


def insert_game_state(game_state):
    """
    Extract data and format it in order to store in the database
    :param game_state: `TotalBotWar.Game.GameState.GameState`
    :return: None
    """

    units = game_state.player_0_units + game_state.player_1_units
    if not os.path.isfile(DB_ROUTE):
        create_db()
        create_table()
    data = units_to_string(units)
    insert_row(*data)


def units_to_string(units):
    """
    Convert a list of units to a list of strings suitable to database format
    :param units: List[`TotalBotWar.Game.Units.Unit.Unit`
    :return: List of strings
    """
    ids = ""
    teams = ""
    healths = ""
    types = ""
    positions = ""
    directions = ""
    states = ""
    for i, unit in enumerate(units):
        ids += str(unit.id)
        teams += str(unit.team)
        healths += str(unit.health)
        types += unit.type
        positions += str(unit.position)
        directions += str(unit.direction)
        states += unit.state
        if i != len(units) - 1:
            ids += ' '
            teams += ' '
            healths += ' '
            types += ' '
            positions += ' '
            directions += ' '
            states += ' '
    return [ids, teams, healths, types, positions, directions, states]
