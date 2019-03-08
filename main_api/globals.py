#
# API for getting globals statistics like:
# the list of all teams, number of players, ...
#

from flask import Blueprint, jsonify
from models.db_engine import engine
from sqlalchemy.sql import text

globals_api = Blueprint('globals_api', __name__)


@globals_api.route('/teams_list', methods=['GET'])
def teams_list():
    conn = engine.connect()

    s = text('SELECT Id, FullName, ShortName, ShortNameAlt FROM Teams')
    result = conn.execute(s)
    conn.close()

    return jsonify([dict(row) for row in result])
