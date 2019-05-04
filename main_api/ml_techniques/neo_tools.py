#
# API For the NEO-SPORTS intelligent tools
#

from flask import Blueprint, jsonify
import pandas as pd
from sklearn.decomposition import PCA
from math import sqrt, pow
from main_api._dataframes import get_one_team_stats_aggregation, get_all_teams_stats_aggregation,\
    better_split_format
from main_api._common_requests_parameters import visualization_columns


neo_tools_api = Blueprint('neo_tools_api', __name__)


# MAGIC WAND FOR A TEAM SEASON
# Shows the strengths and weaknesses of a team season
# Directly offers solutions like kind of player recommendation, stats improvement
@neo_tools_api.route('/wand/team/<team>/<int:year>', methods=['GET'])
def team_magic_wand(team, year):
    data = {}
    the_team_stats = get_one_team_stats_aggregation(team=team, season_begin_year=year)

    if the_team_stats.empty:
        return jsonify(None)

    mean_teams_stats = get_all_teams_stats_aggregation(season_begin_year=year)
    mean_teams_stats = mean_teams_stats.mean()

    stats_compared_to_avg = (the_team_stats - mean_teams_stats).drop(['TeamFullName', 'TeamShortName'], axis=1)
    stats_compared_to_avg = pd.DataFrame(stats_compared_to_avg)
    data['stats_compared_to_avg'] = better_split_format(stats_compared_to_avg.to_dict(orient='split'))

    fg_ratio = (the_team_stats.iloc[0]['FGM'] / the_team_stats.iloc[0]['FGA'])
    ft_ratio = (the_team_stats.iloc[0]['FTM'] / the_team_stats.iloc[0]['FTA'])
    tp_ratio = (the_team_stats.iloc[0]['TPM'] / the_team_stats.iloc[0]['TPA'])

    scorings = ['Field Goals', 'Free Throws', '3 Points']
    ratio = [fg_ratio, ft_ratio, tp_ratio]
    good_ratio = [.48, .78, .37]
    bad_ratio = [.44, .74, .32]

    data['scoring_ratio'] = {
        scorings[0]: fg_ratio,
        scorings[1]: ft_ratio,
        scorings[2]: tp_ratio
    }

    data['scoring_ratio']['improvements'] = []
    for i in range(0, len(scorings)):
        improvement = 'Can do better'
        ratio_rating = 2
        if ratio[i] > good_ratio[i]:
            improvement = 'Very well, keep it up'
            ratio_rating = 3
        elif ratio[i] <= bad_ratio[i]:
            improvement = 'Bad, needs more training in this field.'
            ratio_rating = 1

        data['scoring_ratio']['improvements'].append({
            'field': scorings[i],
            'improvement': improvement,
            'ratio_rating': ratio_rating
        })

    main_stats_improve = stats_compared_to_avg.drop(['FGA', 'FTA', 'TPA', 'Win', 'TF', 'PTS'], axis=1)
    main_stats_improve = (main_stats_improve[main_stats_improve < 0]).dropna(axis=1)

    data['main_stats_to_improve'] = better_split_format(main_stats_improve.to_dict(orient='split'))

    fouls = stats_compared_to_avg['TF'].iloc[0]
    if fouls > 0:
        foul_data = {
            'column': 'TF',
            'data': fouls
        }
        if len(data['main_stats_to_improve']) == 0:
            data['main_stats_to_improve'] = foul_data
        else:
            data['main_stats_to_improve'].append(foul_data)

    data['similars_non_similars_teams'] = _similar_teams(team, year)

    return jsonify(data)


def _similar_teams(team, year, number=3):
    df = get_all_teams_stats_aggregation(season_begin_year=year).sort_index()

    index = df[df['TeamShortName'] == str(team).upper()].index

    teams = df[['TeamFullName', 'TeamShortName']]
    df = df[visualization_columns]

    pca = PCA(n_components=2)
    pca.fit(df)

    points = pca.transform(df)

    team_point = points[index]

    distances = []

    for i in range(0, len(points)):
        distances.append(sqrt(pow(team_point[0, 0] - points[i, 0], 2) + pow(team_point[0, 1] - points[i, 1], 2)))

    teams['Distance'] = distances
    teams = teams.sort_values(by=['Distance'])
    teams = teams.drop(index=index)
    similar_teams = teams.iloc[0:5]
    non_similar_teams = teams.tail(5)

    similars = better_split_format(similar_teams.to_dict(orient='split'))
    non_similars = better_split_format((non_similar_teams.to_dict(orient='split')))

    similars_and_non_similars_teams = {
        'similars': similars,
        'non_similars': non_similars
    }

    return similars_and_non_similars_teams
