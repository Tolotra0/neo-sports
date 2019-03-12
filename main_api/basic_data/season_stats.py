#
# API for getting SEASON statistics
#

from flask import Blueprint, jsonify
from models.db_engine import engine

import pandas as pd
from main_api._dataframes import get_games_stats, get_all_teams_stats_aggregation


season_stats_api = Blueprint('season_stats_api', __name__)


desired_columns = ['TeamFullName', 'TeamShortName', 'FGM', 'FGA', 'TPM', 'TPA', 'FTM',
                   'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'TF', 'PTS', 'Win']

team_columns = ['TeamFullName', 'TeamShortName']


# Get the AVERAGE of total stats for each team in one season
# EXAMPLE: /main/season/2016/avg
# -> Get the AVG of total stats for each team in 2016-2017 season,
# -> ordered by Total Points (TP) (DEFAULT SORTING)
#
@season_stats_api.route('/<int:season_begin_year>/avg', methods=['GET'])
@season_stats_api.route('/<int:season_begin_year>/avg/<string:conference>', methods=['GET'])
def games_average(season_begin_year, conference=None):
    return _season_team_aggregate(season_begin_year, conference, method='MEAN')


@season_stats_api.route('/<int:season_begin_year>/to/<int:season_begin_year2>/avg', methods=['GET'])
@season_stats_api.route('/<int:season_begin_year>/to/<int:season_begin_year2>/avg/<string:conference>', methods=['GET'])
def multiple_games_average(season_begin_year, season_begin_year2, conference=None):
    dataframes = []
    for date in range(season_begin_year, season_begin_year2+1):
        df = get_all_teams_stats_aggregation(season_begin_year, conference=conference, method='MEAN')
        dataframes.append({
            'season': '{}-{}'.format(date, date + 1),
            'data': df.to_dict(orient='records')
        })
    return jsonify(dataframes)


# Get the SUM of total stats for each team in one season
# EXAMPLE: /main/season/2017/sum/east
# -> Get the SUM of total stats for each team in 2017-2018 season,
# -> only for eastern conference teams
#
@season_stats_api.route('/<int:season_begin_year>/sum', methods=['GET'])
@season_stats_api.route('/<int:season_begin_year>/sum/<string:conference>', methods=['GET'])
def games_sum(season_begin_year, conference=None):
    return _season_team_aggregate(season_begin_year, conference, method='SUM')


# Get the global stats average
@season_stats_api.route('/<int:season_begin_year>/global_average', methods=['GET'])
def global_average(season_begin_year):
    df = get_games_stats(season_begin_year=season_begin_year)

    df = df[desired_columns]
    df = df.drop(columns=team_columns)
    df = df.mean()

    print(df)

    return jsonify(df.to_dict())


def _season_team_aggregate(season_begin_year, conference, method='MEAN'):
    df = get_all_teams_stats_aggregation(season_begin_year, conference=conference, method=method)
    print(df)
    return jsonify(df.to_dict(orient='records'))
