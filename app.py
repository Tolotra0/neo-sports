from flask import Flask
import click
from main_api.accounts import accounts_api


app = Flask(__name__)

main_api_url = '/api/main'
mobile_api_url = '/api/mobile'

print(main_api_url+'/accounts')

app.register_blueprint(accounts_api, url_prefix=main_api_url+'/accounts')


@app.route('/')
def application():
    return 'Welcome to the Neo Sports application!'


# -----------------
# Commandline tools
# -----------------

from cmd_tools.game_csv_to_db import game_csv_to_db


@app.cli.command('game_csv_to_db')
@click.option('--path')
def to_db_1(path):
    game_csv_to_db(path)
