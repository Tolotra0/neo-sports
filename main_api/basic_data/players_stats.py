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


# Getting players by ID
@players_stats_api.route('/id/<int:id>', methods=['GET'])
def players_by_id(id):
    df = get_players(id=id)
    print(df)
    return jsonify(df.to_dict(orient='records'))


# Getting season full stats
@players_stats_api.route('/season_stats', methods=['GET'])
@players_stats_api.route('/season_stats/<int:season_begin_year>', methods=['GET'])
def season_stats(season_begin_year=None):
    df = get_players(year=season_begin_year, game_type='regular')

    df = df.drop(['Year', 'GameType', 'Id', 'GameTypeId'], axis=1)
    top = df.sort_values(by=['PTS', 'Salary'], ascending=False)[0:5]

    print(df)

    data = {
        'season': season_begin_year,
        'trends': top.to_dict(orient='records'),
        'stats': {
            'age': df['Age'].tolist(),
            'points': df['PTS'].tolist(),
            'salary': df['Salary'].tolist()
        }
    }

    return jsonify(data)
