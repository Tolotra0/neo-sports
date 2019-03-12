from flask import Flask
import click

from main_api.basic_data.accounts import accounts_api

from main_api.basic_data.game_stats import game_stats_api
from main_api.basic_data.season_stats import season_stats_api
from main_api.basic_data.team_stats import team_stats_api
from main_api.basic_data.globals import globals_api

from main_api.ml_techniques.clustering import clustering_api
from main_api.ml_techniques.visualization import visualization_api

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

main_api_url = '/api/main'
mobile_api_url = '/api/mobile'

# main API blueprints / Basic data API
app.register_blueprint(accounts_api, url_prefix=main_api_url+'/accounts')
app.register_blueprint(game_stats_api, url_prefix=main_api_url+'/games')
app.register_blueprint(season_stats_api, url_prefix=main_api_url+'/season')
app.register_blueprint(team_stats_api, url_prefix=main_api_url+'/team')
app.register_blueprint(globals_api, url_prefix=main_api_url+'/globals')
# main API Blueprints / Machine Learning API
app.register_blueprint(visualization_api, url_prefix=main_api_url+'/visualization')
app.register_blueprint(clustering_api, url_prefix=main_api_url+'/clustering')


@app.route('/')
def application():
    return 'Welcome to the Neo Sports application!'


# -----------------
# Commandline tools
# -----------------

from _cmd_tools.game_csv_to_db import game_csv_to_db


@app.cli.command('game_csv_to_db')
@click.option('--path')
def to_db_1(path):
    game_csv_to_db(path)
