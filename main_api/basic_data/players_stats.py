#
# API for getting players statistics
# Each row is for one player
#

from flask import Blueprint, jsonify
from main_api._dataframes import get_players

players_stats_api = Blueprint('players_stats_api', __name__)


# Getting all the players stats
@players_stats_api.route('/', methods=['GET'])
@players_stats_api.route('/all', methods=['GET'])
def get_all():
    df = get_players()
    print(df)
    return jsonify(df.to_dict(orient='records'))


# Getting players by NAME
@players_stats_api.route('/name/<name>', methods=['GET'])
@players_stats_api.route('/name/<name>/<team>', methods=['GET'])
@players_stats_api.route('/name/<name>/<team>/<int:year>', methods=['GET'])
def players_by_name(name, team=None, year=None):
    df = get_players(name=name, team=team, year=year)
    print(df)
    return jsonify(df.to_dict(orient='records'))


# Getting players by TEAM
@players_stats_api.route('/team/<team>', methods=['GET'])
@players_stats_api.route('/team/<team>/<int:year>', methods=['GET'])
@players_stats_api.route('/team/<team>/<int:year>/<game_type>', methods=['GET'])
def players_by_team(team, year=None, game_type=None):
    df = get_players(team=team, year=year, game_type=game_type)
    print(df)
    return jsonify(df.to_dict(orient='records'))
