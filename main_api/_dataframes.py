#
# COMMON DATAFRAMES DATABASE REQUESTS
# -> Returns dataframes -> for data manipulation or in algorithm usage
# -> Can also used for getting API datas
#

import pandas as pd
from models.db_engine import engine
from sqlalchemy.sql import text

from main_api._common_requests_parameters import base_game_request, \
    season_start_month, season_end_month, season_filter, sorting, player_request


team_filter = ' Team.ShortName = :team '
year_filter = ' YEAR(Games.Date) = :year '
month_filter = ' MONTH(Games.Date) = :month '
day_filter = ' DAY(Games.Date) = :day '
conference_filter = ' TeamConf.Name = :conference '
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

    parameters = [season_begin_year, conference, team, year, month, day]
    parameters_keys = ['season', 'conference', 'team', 'year', 'month', 'day']
    add_parameters = [p is not None for p in parameters]
    filters = [season_filter, conference_filter, team_filter, year_filter, month_filter, day_filter]

    request = base_game_request
    init_request = request
    request_parameters = {}

    for i, add in enumerate(add_parameters):
        if add:
            if i == 0:
                request_parameters['beginYear'] = season_begin_year
                request_parameters['beginMonth'] = season_start_month
                request_parameters['endYear'] = season_begin_year + 1
                request_parameters['endMonth'] = season_end_month
            else:
                request_parameters[parameters_keys[i]] = parameters[i]

            if request == init_request:
                request = request + _where_ + filters[i]
            else:
                request = request + _and_ + filters[i]

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

def get_players(name=None, year=None, age=None, position=None, team=None, game_type=None):
    conn = engine.connect()

    df = pd.read_sql(text(player_request), conn, params={
        'name': name,
        'year': year,
        'age': age,
        'team': team,
        'game_type': game_type
    })

    conn.close()
    return df
