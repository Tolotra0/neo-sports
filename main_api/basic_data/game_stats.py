#
# API for getting GAMES statistics
# Stats given here are for ONE team
#

from flask import Blueprint, jsonify
from main_api._dataframes import get_games_stats


game_stats_api = Blueprint('game_stats_api', __name__)


@game_stats_api.route('/', methods=['GET'])
@game_stats_api.route('/all', methods=['GET'])
def get_all():
    df = get_games_stats()
    print(df)
    json = df.to_json(orient='records')
    return jsonify(json)


# EXAMPLE: /-team/CLE/2016/12/25
# -> CLE game for 25 December 2016
#
@game_stats_api.route('/team/<string:team>', methods=['GET'])
@game_stats_api.route('/team/<string:team>/<int:year>', methods=['GET'])
@game_stats_api.route('/team/<string:team>/<int:year>/<int:month>', methods=['GET'])
@game_stats_api.route('/team/<string:team>/<int:year>/<int:month>/<int:day>', methods=['GET'])
def teams(team, year=None, month=None, day=None):
    df = get_games_stats(team=team, year=year, month=month, day=day)
    print(df)
    return jsonify(df.to_dict(orient='records'))


# EXAMPLES:
# /main/games/season/2017
# -> 2017-2018 season's games
# /main/games/season/2017/TOR
# -> 2017-2018 season's games for Toronto Raptors
#
@game_stats_api.route('/season/<int:season_begin_year>', methods=['GET'])
@game_stats_api.route('/season/<int:season_begin_year>/<string:team>', methods=['GET'])
def season(season_begin_year, team=None):
    df = get_games_stats(season_begin_year=season_begin_year, team=team)
    print(df)
    return jsonify(df.to_dict(orient='records'))
