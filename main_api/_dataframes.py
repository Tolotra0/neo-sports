#
# COMMON DATAFRAMES DATABASE REQUESTS
# -> Returns dataframes -> for data manipulation or in algorithm usage
# -> Can also used for getting API datas
#

import pandas as pd
import numpy as np
from models.db_engine import engine
from sqlalchemy.sql import text

from main_api._common_requests_parameters import base_game_request, \
    season_start_month, season_end_month, season_filter, sorting, player_request


_and_ = ' AND '
_where_ = ' WHERE '

aggregation_columns = ['TeamFullName', 'TeamShortName', 'FGM', 'FGA', 'TPM', 'TPA', 'FTM',
                       'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'TF', 'PTS', 'Win']

team_columns = ['TeamFullName', 'TeamShortName']


# !!!! IMPORTANT !!!!
# For better usage, use identifiers when passing parameters
# EXAMPLE: df = get_games_stats(year='2016', team='TOR')
# !!!! IMPORTANT !!!!

def get_games_stats(season_begin_year=None, conference=None, team=None, year=None, month=None, day=None):
    # USELESS PARAMETERS COMBINATION
    if all([v is not None for v in [conference, team]]):
        return 'ERROR - get_games_stats(): Useless parameters combination => conference and team.'

    request = base_game_request

    request_parameters = {
        'conference': conference,
        'team': team,
        'year': year,
        'month': month,
        'day': day
    }

    if season_begin_year is not None:
        request = request + _and_ + season_filter
        request_parameters['beginYear'] = season_begin_year
        request_parameters['beginMonth'] = season_start_month
        request_parameters['endYear'] = season_begin_year + 1
        request_parameters['endMonth'] = season_end_month

    conn = engine.connect()

    s = text(request + sorting)

    df = pd.read_sql(s, conn, params=request_parameters)

    conn.close()
    return df


def get_all_teams_stats_aggregation(season_begin_year=None, conference=None, method='MEAN'):
    df = get_games_stats(season_begin_year=season_begin_year, conference=conference)

    if df.empty:
        return df

    df = df[aggregation_columns]

    if method == 'SUM':
        df = pd.DataFrame(df.groupby(by=team_columns, as_index=False).sum())
    elif method == 'MEAN':
        df = pd.DataFrame(df.groupby(by=team_columns, as_index=False).mean())

    df = df.sort_values(by=['PTS'], ascending=False)

    return df


def get_one_team_stats_aggregation(team, season_begin_year=None, method='MEAN'):
    df = get_games_stats(team=team, season_begin_year=season_begin_year)

    if df.empty:
        return df

    df = df[aggregation_columns]

    if method == 'SUM':
        df = pd.DataFrame(df.groupby(by=team_columns, as_index=False).sum())
    elif method == 'MEAN':
        df = pd.DataFrame(df.groupby(by=team_columns, as_index=False).mean())

    df = df.sort_values(by=['PTS'], ascending=False)

    return df


#
# PLAYERS DATA
#

def get_players(name=None, year=None, age=None, position=None, team=None, game_type=None, id=None):
    conn = engine.connect()

    df = pd.read_sql(text(player_request), conn, params={
        'name': name,
        'year': year,
        'age': age,
        'team': team,
        'game_type': game_type,
        'id': id
    })

    df = df.replace({np.nan: None})

    conn.close()
    return df


#
# TEAMS DATA
#
# Team information
def get_team_info(team):
    conn = engine.connect()

    request = 'SELECT Teams.*, Cities.Name AS City, Divisions.Name AS Division, Conferences.Name AS Conference ' \
              'FROM Teams JOIN Cities JOIN Divisions JOIN Conferences ' \
              'ON Teams.CityId = Cities.Id AND Cities.DivisionId = Divisions.Id ' \
              'AND Divisions.ConferenceId = Conferences.Id ' \
              'WHERE Teams.ShortName = :team OR Teams.ShortNameAlt = :team '

    df = pd.read_sql(text(request), conn, params={'team': team})

    return df


# Team points per date for one season
def get_team_points_per_date(team, season):
    df = get_games_stats(season_begin_year=season, team=team)
    df = df[['Date', 'PTS']]
    return df


# Team win and lose in a season
def get_team_win_lose(team, season):
    df = get_games_stats(season_begin_year=season, team=team)
    df = df[['TeamFullName', 'TeamShortName', 'Win']]
    total = len(df)
    df = df.groupby(by=['TeamShortName', 'TeamFullName'], as_index=False).sum()
    df['Lose'] = total - df['Win']

    return pd.DataFrame(df)


#
# UTILITIES
#
def better_split_format(dictionary):
    columns = dictionary['columns']
    data = dictionary['data']
    ncol = len(columns)
    ndata = len(data)

    print(dictionary)
    result = []

    for i in range(0, ndata):
        result.append([{'column': columns[j], 'data': data[i][j]} for j in range(0, ncol)])

    if len(result) == 1:
        return result[0]
    return result
