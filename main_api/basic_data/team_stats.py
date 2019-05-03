#
# API For getting ONE TEAM statistics
#

from flask import Blueprint, jsonify
import pandas as pd
from main_api._dataframes import get_games_stats, get_team_info, get_team_points_per_date,\
    get_team_win_lose, get_one_team_stats_aggregation, get_players


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


# Gets the team points per date
@team_stats_api.route('/<string:team>/<int:season_begin_year>/points_per_date')
def season_points_per_date(team, season_begin_year):
    df = get_team_points_per_date(team=team, season=season_begin_year)
    print(df)
    return jsonify(df.to_dict(orient='records'))


# Gets the team win lose in a season
@team_stats_api.route('/<string:team>/<int:season_begin_year>/win_lose')
def season_win_lose(team, season_begin_year):
    df = get_team_win_lose(team=team, season=season_begin_year)
    print(df)
    return jsonify(df.to_dict(orient='records'))


# Team full stats for one season
@team_stats_api.route('/<string:team>/<int:season_begin_year>/full_stats')
def season_full_stats(team, season_begin_year):
    team_info = get_team_info(team=team)
    team_info = team_info.to_dict(orient='records')[0]
    team_info['season'] = season_begin_year

    points_per_date = get_team_points_per_date(team=team, season=season_begin_year)
    team_info['points_per_date'] = points_per_date.to_dict(orient='records')

    win_lose = get_team_win_lose(team=team, season=season_begin_year)[['Win', 'Lose']].to_dict(orient='records')[0]
    win_lose['Win'] = int(win_lose['Win'])
    win_lose['Lose'] = int(win_lose['Lose'])
    team_info['win_lose'] = win_lose

    performances = get_one_team_stats_aggregation(team=team, season_begin_year=season_begin_year)
    performances = performances.drop(['TeamFullName', 'TeamShortName'], axis=1)
    team_info['performances'] = performances.to_dict(orient='split')
    subjects = team_info['performances']['columns']
    values = team_info['performances']['data'][0]
    team_info['performances'] = [{'subject': subjects[i], 'value': values[i]} for i in range(0, len(subjects))]

    players = get_players(team=team, year=season_begin_year, game_type='regular')
    players = players.drop(['TeamId', 'TeamFullName', 'TeamAbbr', 'Id', 'GameTypeId', 'GameType', 'Year'], axis=1)
    players_info = players[['PlayerId', 'Name', 'Age']].to_dict(orient='records')
    players_stats = players.drop(['PlayerId', 'Name', 'Age'], axis=1).to_dict(orient='split')
    player_stats_columns = players_stats['columns']
    players_stats_data = players_stats['data']
    ncol = len(player_stats_columns)
    nplayers = len(players_stats_data)
    for i in range(0, nplayers):
        players_info[i]['stats'] = [{'subject': player_stats_columns[j], 'value': players_stats_data[i][j]}
                                    for j in range(0, ncol)]
    team_info['players'] = players_info

    return jsonify(team_info)


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
