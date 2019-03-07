from flask import Blueprint, jsonify, request
from models.db_engine import engine
from sqlalchemy.sql import text

game_stats_api = Blueprint('game_stats_api', __name__)


season_start_month = 10
season_end_month = 4


# Note the aliases in the two Teams tables: Team and Opponents
base_game_request = 'SELECT Games.Date, Games.Duration, Games.Win, Team.FullName AS TeamFullName, \
                Team.ShortName TeamShortName, Opponent.FullName AS OpFullName, \
                Opponent.ShortName AS OpShortName, TeamGameStats.*, \
                GameTypes.Type AS GameType, GameLocationTypes.LocationType FROM Games \
                JOIN Teams Team ON Games.TeamId = Team.Id \
                JOIN Teams Opponent ON Opponent.Id = Games.OpponentId \
                JOIN TeamGameStats ON Games.Id = TeamGameStats.GameId \
                JOIN GameTypes ON Games.GameTypeId = GameTypes.Id \
                JOIN GameLocationTypes ON Games.GameLocationTypeId = GameLocationTypes.Id'

sorting = ' ORDER BY Team.Id, Games.Date '


@game_stats_api.route('/', methods=['GET'])
@game_stats_api.route('/all', methods=['GET'])
def get_all():
    conn = engine.connect()

    s = text(base_game_request + sorting)

    result = conn.execute(s)
    conn.close()

    return jsonify([dict(row) for row in result])


# EXAMPLE: /api/games/CLE/2016/12/25
# -> CLE game for 25 December 2016
@game_stats_api.route('/<string:team>', methods=['GET'])
@game_stats_api.route('/<string:team>/<int:year>', methods=['GET'])
@game_stats_api.route('/<string:team>/<int:year>/<int:month>', methods=['GET'])
@game_stats_api.route('/<string:team>/<int:year>/<int:month>/<int:day>', methods=['GET'])
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
        return jsonify({'result': None})

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


@game_stats_api.route('/season/<int:begin_year>')
def season(begin_year):
    conn = engine.connect()

    s = text(base_game_request +
             ' WHERE (YEAR(Games.Date) = :beginYear AND MONTH(Games.Date) >= :beginMonth) \
              OR (YEAR(Games.Date) = :endYear AND MONTH(Games.Date) <= :endMonth) '
             + sorting)

    result = conn.execute(s, beginYear=begin_year, beginMonth=season_start_month,
                          endYear=begin_year+1, endMonth=season_end_month)

    conn.close()
    return jsonify([dict(row) for row in result])
