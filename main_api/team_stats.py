#
# API For getting ONE TEAM statistics
#

from flask import Blueprint, jsonify
from models.db_engine import engine
from sqlalchemy.sql import text

import pandas as pd

from main_api._common_requests_parameters import base_game_request, \
    season_start_month, season_end_month, season_filter

team_stats_api = Blueprint('team_stats_api', __name__)

game_columns = ['Duration', 'Win', 'TeamFullName', 'TeamShortName',
                'GameType', 'LocationType']

grouping_columns = ['TeamShortName', 'TeamFullName', 'GameType', 'LocationType']

team_filter_req = ' Team.ShortName = :team '

main_req = base_game_request


# Gets all time games resume for the team
# EXAMPLE: /main/team/GSW/alltime/games_resume
# -> Get all time season game resume for GSW
@team_stats_api.route('/<string:team>/alltime/games_resume', methods=['GET'])
def alltime_games_resume(team):
    return _games_resume(team)


# Gets the season games resume for the team
# EXAMPLE: /main/team/GSW/2016/games_resume
# -> Get the 2016-2017 season game resume for GSW
@team_stats_api.route('/<string:team>/<int:begin_year>/games_resume', methods=['GET'])
def season_games_resume(team, begin_year):
    return _games_resume(team, begin_year)


def _games_resume(team, begin_year=None):
    conn = engine.connect()
    df = pd.DataFrame()

    if begin_year is None:
        s = text(main_req + ' WHERE ' + team_filter_req)
        df = pd.read_sql(s, conn, params={'team': team})
    else:
        s = text(main_req + season_filter + ' AND ' + team_filter_req)
        df = pd.read_sql(s, conn, params={
            'team': team,
            'beginYear': begin_year,
            'beginMonth': season_start_month,
            'endYear': begin_year + 1,
            'endMonth': season_end_month
        })

    df = df[game_columns]

    homesDf = df[df['LocationType'] == 'Home']
    awaysDf = df[df['LocationType'] == 'Away']

    games_played_home = len(homesDf)
    games_played_away = len(awaysDf)

    homesDf = homesDf.groupby(by=grouping_columns, as_index=False).sum()
    awaysDf = awaysDf.groupby(by=grouping_columns, as_index=False).sum()

    homesDf['Lose'] = games_played_home - homesDf['Win']
    awaysDf['Lose'] = games_played_away - awaysDf['Win']

    homes = homesDf.to_json(orient='records')
    aways = awaysDf.to_json(orient='records')

    conn.close()

    return jsonify(homes, aways)
