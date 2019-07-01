from flask import Flask
import click

from main_api.basic_data.accounts import accounts_api

from main_api.basic_data.game_stats import game_stats_api
from main_api.basic_data.season_stats import season_stats_api
from main_api.basic_data.team_stats import team_stats_api
from main_api.basic_data.players_stats import players_stats_api
from main_api.basic_data.globals import globals_api

from main_api.ml_techniques.clustering import clustering_api
from main_api.ml_techniques.visualization import visualization_api
from main_api.ml_techniques.prediction import prediction_api

from main_api.ml_techniques.neo_tools import neo_tools_api

from mobile_api.mobile_app import mobile_api

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

main_api_url = '/api/main'
mobile_api_url = '/api/mobile'

# main API blueprints / Basic data API
app.register_blueprint(accounts_api, url_prefix=main_api_url+'/accounts')
app.register_blueprint(game_stats_api, url_prefix=main_api_url+'/games')
app.register_blueprint(season_stats_api, url_prefix=main_api_url+'/season')
app.register_blueprint(team_stats_api, url_prefix=main_api_url+'/team')
app.register_blueprint(players_stats_api, url_prefix=main_api_url+'/players')
app.register_blueprint(globals_api, url_prefix=main_api_url+'/globals')
# main API Blueprints / Machine Learning API
app.register_blueprint(visualization_api, url_prefix=main_api_url+'/visualization')
app.register_blueprint(clustering_api, url_prefix=main_api_url+'/clustering')
app.register_blueprint(prediction_api, url_prefix=main_api_url+'/prediction')

# The NEO TOOLS API
app.register_blueprint(neo_tools_api, url_prefix=main_api_url+'/neotools')

# mobile api blueprints
app.register_blueprint(mobile_api, url_prefix=mobile_api_url)


@app.route('/')
def application():
    return 'Welcome to the Neo Sports application!'


# -----------------
# Commandline tools
# -----------------

from _cmd_tools.game_csv_to_db import game_csv_to_db
from _cmd_tools.players_csv_to_db import players_csv_to_db
from _cmd_tools.salaries_csv_to_db import salaries_csv_to_db


@app.cli.command('game-csv-to-db')
@click.option('--path')
def to_db_1(path):
    game_csv_to_db(path)


# EXAMPLE - In terminal, type:
# > flask players-csv-to-db --path='_csv_files/players_playoffs/2017-18.csv' --game-type='Playoffs' --year=2017
@app.cli.command('players-csv-to-db')
@click.option('--path')
@click.option('--year')
@click.option('--game-type')
def to_db_2(path, year, game_type):
    if year is None:
        print('ERROR: You must specify a season begin year with --year option.')
        return

    try:
        year = int(year)
    except Exception:
        print('ERROR: Invalid year value.')
        return

    types = ['Regular Season', 'Playoffs']

    if not any([game_type == type for type in types]):
        print('ERROR: Invalid game types. You shoud choose between ', types)
        return

    for i, type in enumerate(types):
        if type == game_type:
            game_type = i + 1

    players_csv_to_db(path, year, game_type)


# Player salaries import
@app.cli.command('players-salaries-to-db')
@click.option('--path')
@click.option('--year')
def to_db_3(path, year):
    if year is None:
        print('ERROR: You must specify a season begin year with --year option.')
        return

    try:
        year = int(year)
    except Exception:
        print('ERROR: Invalid year value.')
        return

    salaries_csv_to_db(path, year)
