#
# API for getting data visualizations like:
# points, charts, polars, and so on ...
#

from flask import Blueprint, jsonify
from sklearn.decomposition import PCA

from main_api._dataframes import get_all_teams_stats_aggregation, get_players
from main_api._common_requests_parameters import visualization_columns, player_visualization_columns


visualization_api = Blueprint('visualization_api', __name__)


# API for getting multiple TEAMS visualization with POINTS
# EXAMPLE: /main/visualization/points/teams/2017/east
# -> All eastern teams points visualization for 2017-2018 season
#
@visualization_api.route('/points/teams', methods=['GET'])
@visualization_api.route('/points/teams/<int:season_begin_year>', methods=['GET'])
@visualization_api.route('/points/teams/<int:season_begin_year>/<string:conference>', methods=['GET'])
def points_teams(season_begin_year=None, conference=None):
    df = get_all_teams_stats_aggregation(season_begin_year=season_begin_year, conference=conference)

    if df.empty:
        return jsonify(None)

    print(df)

    teams = df['TeamShortName']

    df = df[visualization_columns]

    pca = PCA(n_components=2)
    pca.fit(df)

    points_2d = pca.transform(df)

    return jsonify(teams.tolist(), points_2d.tolist())


# API for getting PLAYERS visualization with POINTS
# FOR A TEAM
@visualization_api.route('/points/players/team/<team>/<int:season_begin_year>', methods=['GET'])
def team_players(team, season_begin_year):
    df = get_players(team=team, year=season_begin_year, game_type='regular')

    if df.empty:
        return jsonify(None)

    print(df)

    names = df['Name']

    df = df[player_visualization_columns]
    pca = PCA(n_components=2)
    pca.fit(df)
    points_2d = pca.transform(df)

    return jsonify(names.tolist(), points_2d.tolist())


# API for getting PLAYERS visualization with POINTS
# FOR A SEASON
@visualization_api.route('/points/players/season/<int:season_begin_year>', methods=['GET'])
def season_players(season_begin_year):
    df = get_players(year=season_begin_year, game_type='regular')

    if df.empty:
        return jsonify(None)

    print(df)

    names = df['Name']

    df = df[player_visualization_columns]
    pca = PCA(n_components=2)
    pca.fit(df)
    points_2d = pca.transform(df)

    return jsonify(names.tolist(), points_2d.tolist())
