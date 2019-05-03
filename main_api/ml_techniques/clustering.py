#
# API for getting different sorts of clustering like:
# teams clustering, players clustering, and so on ...
#

from flask import Blueprint, jsonify
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from main_api._dataframes import get_all_teams_stats_aggregation, get_players
from main_api._common_requests_parameters import visualization_columns, player_visualization_columns


clustering_api = Blueprint('clustering_api', __name__)


# API for getting teams clustering based on multiple parameters
# EXAMPLE: /main/clustering/teams/3/2016
# -> Get the teams' clustering based by stats, for 2016-2017 season, k=3
#
@clustering_api.route('/teams', methods=['GET'])
@clustering_api.route('/teams/<int:k>/<int:season_begin_year>', methods=['GET'])
@clustering_api.route('/teams/<int:k>/<int:season_begin_year>/<string:conference>', methods=['GET'])
def teams_clustering(k=4, season_begin_year=None, conference=None):
    df = get_all_teams_stats_aggregation(season_begin_year=season_begin_year, conference=conference)

    if df.empty:
        return jsonify(None)

    print(df)

    teams = df['TeamShortName']

    df = df[visualization_columns]

    pca = PCA(n_components=2)
    pca.fit(df)

    points_2d = pca.transform(df)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points_2d)
    cluster_labels = kmeans.labels_

    return jsonify(teams.tolist(), points_2d.tolist(), cluster_labels.tolist())


# API for getting PLAYERS CLUSTERING
# FOR A TEAM
@clustering_api.route('/players/<int:k>/team/<team>/<int:season_begin_year>', methods=['GET'])
def team_players(k, team, season_begin_year):
    df = get_players(team=team, year=season_begin_year, game_type='regular')

    if df.empty:
        return jsonify(None)

    print(df)

    names = df['Name']

    df = df[player_visualization_columns]
    pca = PCA(n_components=2)
    pca.fit(df)
    points_2d = pca.transform(df)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points_2d)
    cluster_labels = kmeans.labels_

    return jsonify(names.tolist(), points_2d.tolist(), cluster_labels.tolist())


# API for getting PLAYERS CLUSTERING
# FOR A SEASON
@clustering_api.route('players/<int:k>/season/<int:season_begin_year>', methods=['GET'])
def season_players(k, season_begin_year):
    df = get_players(year=season_begin_year, game_type='regular')

    if df.empty:
        return jsonify(None)

    print(df)

    names = df['Name']

    df = df[player_visualization_columns]
    pca = PCA(n_components=2)
    pca.fit(df)
    points_2d = pca.transform(df)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points_2d)
    cluster_labels = kmeans.labels_

    return jsonify(names.tolist(), points_2d.tolist(), cluster_labels.tolist())
