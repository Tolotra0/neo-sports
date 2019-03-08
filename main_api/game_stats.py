#
# API for getting games statistics
# Stats given here are for ONE team
#

from flask import Blueprint, jsonify
from models.db_engine import engine
from sqlalchemy.sql import text

from main_api._common_requests_parameters import base_game_request, sorting, \
    season_start_month, season_end_month, season_filter

game_stats_api = Blueprint('game_stats_api', __name__)


@game_stats_api.route('/', methods=['GET'])
@game_stats_api.route('/all', methods=['GET'])
def get_all():
    conn = engine.connect()

    s = text(base_game_request + sorting)

    result = conn.execute(s)
    conn.close()

    return jsonify([dict(row) for row in result])


# EXAMPLE: /api/games/team/CLE/2016/12/25
# -> CLE game for 25 December 2016
#
@game_stats_api.route('/team/<string:team>', methods=['GET'])
@game_stats_api.route('/team/<string:team>/<int:year>', methods=['GET'])
@game_stats_api.route('/team/<string:team>/<int:year>/<int:month>', methods=['GET'])
@game_stats_api.route('/team/<string:team>/<int:year>/<int:month>/<int:day>', methods=['GET'])
def teams(team, year=None, month=None, day=None):
    conn = engine.connect()
    s = None
    result = None

    team_id = conn.execute(text('SELECT Id FROM Teams WHERE ShortName = :x'), x=team).fetchone()

    if team_id is not None:
        team_id = team_id['Id']
        s = base_game_request + ' WHERE Team.Id = :id '

    if year is not None:
        s = s + ' AND YEAR(Games.Date) = :year '
    if month is not None:
        s = s + ' AND MONTH(Games.Date) = :month '
    if day is not None:
        s = s + ' AND DAY(Games.Date) = :day '

    if s is None:
        return jsonify(None)

    s = text(s + sorting)

    if year is None:
        result = conn.execute(s, id=team_id)
    elif year is not None and month is None and day is None:
        result = conn.execute(s, id=team_id, year=year)
    elif year is not None and month is not None and day is None:
        result = conn.execute(s, id=team_id, year=year, month=month)
    else:
        result = conn.execute(s, id=team_id, year=year, month=month, day=day)

    conn.close()
    return jsonify([dict(row) for row in result])


# EXAMPLES:
# /api/games/season/2017
# -> 2017-2018 season's games
# /api/games/season/2017/TOR
# -> 2017-2018 season's games for Toronto Raptors
#
@game_stats_api.route('/season/<int:begin_year>', methods=['GET'])
@game_stats_api.route('/season/<int:begin_year>/<string:team>', methods=['GET'])
def season(begin_year, team=None):
    conn = engine.connect()

    result = None

    s = base_game_request + season_filter

    if team is None:
        s = text(s + sorting)
        result = conn.execute(s, beginYear=begin_year, beginMonth=season_start_month,
                              endYear=begin_year + 1, endMonth=season_end_month)

    else:
        team_id = conn.execute(text('SELECT Id FROM Teams WHERE ShortName = :x'), x=team).fetchone()

        if team_id is not None:
            team_id = team_id['Id']
            s = text(s + ' AND Team.Id = :id ' + sorting)

            result = conn.execute(s, beginYear=begin_year, beginMonth=season_start_month,
                                  endYear=begin_year + 1, endMonth=season_end_month, id=team_id)

    conn.close()

    if result is None:
        return jsonify(None)

    return jsonify([dict(row) for row in result])
