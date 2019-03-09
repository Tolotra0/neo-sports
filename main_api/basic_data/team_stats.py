#
# API For getting ONE TEAM statistics
#

from flask import Blueprint, jsonify
import pandas as pd
from main_api._dataframes import get_games_stats


team_stats_api = Blueprint('team_stats_api', __name__)


grouping_columns = ['TeamShortName', 'TeamFullName', 'GameType', 'LocationType']


# Gets all time games resume for the team
# EXAMPLE: /main/team/GSW/alltime/games_resume
# -> Get all time season game resume for GSW
@team_stats_api.route('/<string:team>/alltime/games_resume', methods=['GET'])
def alltime_games_resume(team):
    return _games_resume(team)


# Gets the season games resume for the team
# EXAMPLE: /main/team/GSW/2016/games_resume
# -> Get the 2016-2017 season game resume for GSW
@team_stats_api.route('/<string:team>/<int:season_begin_year>/games_resume', methods=['GET'])
def season_games_resume(team, season_begin_year):
    return _games_resume(team, season_begin_year)


# Gets all time games stats average for the team
# EXAMPLE: /main/team/HOU/alltime/games_stats_avg
# -> Get all time game stats average for the Houston Rockets
@team_stats_api.route('/<string:team>/alltime/games_stats_avg')
def alltime_game_stats_avg(team):
    return _game_stats_average(team)


# Gets the season games stats average for the team
# EXAMPLE: /main/team/HOU/2014/games_stats_avg
# -> Get the 2014-2015 season game stats average for the Houston Rockets
@team_stats_api.route('/<string:team>/<int:season_begin_year>/games_stats_avg')
def season_game_stats_avg(team, season_begin_year):
    return _game_stats_average(team, season_begin_year)


def _games_resume(team, season_begin_year=None):
    game_columns = ['Duration', 'Win', 'TeamFullName', 'TeamShortName',
                    'GameType', 'LocationType']

    df = get_games_stats(team=team)
    if season_begin_year is not None:
        df = get_games_stats(season_begin_year=season_begin_year, team=team)

    df = df[game_columns]

    homesDf = df[df['LocationType'] == 'Home']
    awaysDf = df[df['LocationType'] == 'Away']

    games_played_home = len(homesDf)
    games_played_away = len(awaysDf)

    homesDf = homesDf.groupby(by=grouping_columns, as_index=False).sum()
    awaysDf = awaysDf.groupby(by=grouping_columns, as_index=False).sum()

    homesDf['Lose'] = games_played_home - homesDf['Win']
    awaysDf['Lose'] = games_played_away - awaysDf['Win']

    df = homesDf.append(awaysDf)

    print(df)

    return jsonify(df.to_dict(orient='records'))


def _game_stats_average(team, season_begin_year=None):
    desired_columns = ['TeamFullName', 'TeamShortName', 'FGM', 'FGA', 'TPM', 'TPA', 'FTM',
                       'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'TF', 'PTS']

    df = get_games_stats(team=team)

    if season_begin_year is not None:
        df = get_games_stats(season_begin_year=season_begin_year, team=team)

    df = df[desired_columns]

    df = pd.DataFrame(df.groupby(by=['TeamFullName', 'TeamShortName'], as_index=False).mean())

    print(df)

    return jsonify(df.to_dict(orient='records'))
