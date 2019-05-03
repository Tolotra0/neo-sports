#
# API for sending data collected with the mobile app
#

from flask import Blueprint, jsonify, request
from models.db_models import Game, TeamGameStat, Team, GameLocationType
from models.db_engine import engine
from sqlalchemy.orm import sessionmaker
import datetime


mobile_api = Blueprint('mobile_api', __name__)

Session = sessionmaker(bind=engine)


@mobile_api.route('/add_game', methods=['POST'])
def add_game():
    message = 'Row successfully inserted.'

    if request.method == 'POST':
        game = _generate_game_class(request.form)
        game_stats = _generate_game_stats_class(request.form)

        if any([value is None for value in [game, game_stats]]):
            message = 'An error occured, please check your data values.'
            return jsonify({'success': False, 'message': message})

        session = Session()

        session.add(game)
        session.flush()

        game_stats.GameId = game.Id
        session.add(game_stats)
        session.flush()

        session.commit()

        return jsonify({'success': True, 'message': message})

    return jsonify({'success': False, 'message': 'Permission Denied.'})


def _generate_game_class(form):
    session = Session()

    team_id = session.query(Team.Id).filter(Team.ShortName == form['Team']).first()
    opponent_id = session.query(Team.Id).filter(Team.ShortName == form['Opponent']).first()
    game_location_type_id = session.query(GameLocationType.Id)\
        .filter(GameLocationType.LocationType == form['GameLocationType']).first()

    if any([value is None for value in [team_id, opponent_id, game_location_type_id]]):
        return None

    game = Game()

    try:
        game.Date = datetime.datetime.strptime(form['Date'], '%Y-%m-%d')
        game.Duration = None
        game.TeamId = team_id.Id
        game.OpponentId = opponent_id.Id
        game.GameTypeId = 1  # REGULAR SEASON FOR NOW
        game.GameLocationTypeId = game_location_type_id.Id
        game.Win = int(form['Win'])
    except Exception:
        return None

    if game.Date is None:
        return None

    return game


def _generate_game_stats_class(row):
    game_stat = TeamGameStat()

    try:
        game_stat.PTS = int(row['PTS'])
        game_stat.FGM = int(row['FGM'])
        game_stat.FGA = int(row['FGA'])
        game_stat.TPM = int(row['TPM'])
        game_stat.TPA = int(row['TPA'])
        game_stat.FTM = int(row['FTM'])
        game_stat.FTA = int(row['FTA'])
        game_stat.OREB = int(row['OREB'])
        game_stat.DREB = int(row['DREB'])
        game_stat.AST = int(row['AST'])
        game_stat.STL = int(row['STL'])
        game_stat.BLK = int(row['BLK'])
        game_stat.TOV = int(row['TOV'])
        game_stat.TF = int(row['TF'])
    except Exception:
        return None

    return game_stat
