#
# API for getting globals statistics like:
# the list of all teams, number of players, ...
#

from flask import Blueprint, jsonify
from models.db_engine import engine
from sqlalchemy.sql import text

from main_api._dataframes import get_team_info


globals_api = Blueprint('globals_api', __name__)


# List of all teams
@globals_api.route('/teams/list', methods=['GET'])
def teams_list():
    conn = engine.connect()

    s = text('SELECT Id, FullName, ShortName, ShortNameAlt FROM Teams')
    result = conn.execute(s)
    conn.close()

    return jsonify([dict(row) for row in result])


# Getting one team information
@globals_api.route('/teams/info/<team>')
def team_info(team):
    df = get_team_info(team)
    df = df.to_dict(orient='records')
    print(df[0])
    return jsonify(df[0])
