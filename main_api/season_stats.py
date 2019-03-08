#
# API for getting season statistics
#

from flask import Blueprint, jsonify
from models.db_engine import engine
from sqlalchemy.sql import text

import pandas as pd

from main_api._common_requests_parameters import base_game_request, \
    season_start_month, season_end_month, season_filter

season_stats_api = Blueprint('season_stats_api', __name__)


main_req = base_game_request + season_filter
by_conference_req = ' AND TeamConf.Name = :conference '

desired_columns = ['TeamFullName', 'TeamShortName', 'FGM', 'FGA', 'TPM', 'TPA', 'FTM',
                   'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'TF', 'PTS', 'Win']

team_columns = ['TeamFullName', 'TeamShortName']


# Get the AVERAGE of total stats for each team in one season
# EXAMPLE: /season/2016/avg
# -> Get the AVG of total stats for each team in 2016-2017 season,
# -> ordered by Total Points (TP) (DEFAULT SORTING)
#
@season_stats_api.route('/<int:begin_year>/avg', methods=['GET'])
@season_stats_api.route('/<int:begin_year>/avg/<string:conference>', methods=['GET'])
def games_average(begin_year, conference=None):
    return _season_team_aggregate(begin_year, conference, method='MEAN')


# Get the SUM of total stats for each team in one season
# EXAMPLE: /season/2017/sum/east
# -> Get the SUM of total stats for each team in 2017-2018 season,
# -> ordered by Assist (AST)
#
@season_stats_api.route('/<int:begin_year>/sum', methods=['GET'])
@season_stats_api.route('/<int:begin_year>/sum/<string:conference>', methods=['GET'])
def games_sum(begin_year, conference=None):
    return _season_team_aggregate(begin_year, conference, method='SUM')


def _season_team_aggregate(begin_year, conference, method='SUM'):
    conn = engine.connect()

    s = text(main_req)
    df = pd.read_sql(s, conn, params={
        'beginYear': begin_year,
        'beginMonth': season_start_month,
        'endYear': begin_year + 1,
        'endMonth': season_end_month
    })

    if conference is not None:
        s = text(main_req + by_conference_req)
        df = pd.read_sql(s, conn, params={
            'beginYear': begin_year,
            'beginMonth': season_start_month,
            'endYear': begin_year + 1,
            'endMonth': season_end_month,
            'conference': conference
        })

    df = df[desired_columns]

    if method == 'SUM':
        df = pd.DataFrame(df.groupby(by=team_columns, as_index=False).sum())
    elif method == 'MEAN':
        df = pd.DataFrame(df.groupby(by=team_columns, as_index=False).mean())

    df = df.sort_values(by=['PTS'], ascending=False)

    print(df)

    json = df.to_json(orient='records')
    return jsonify(json)
