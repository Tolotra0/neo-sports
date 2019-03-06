from flask import Flask

from main_api.accounts import accounts_api


app = Flask(__name__)

main_api_url = '/api/main'
mobile_api_url = '/api/mobile'

print(main_api_url+'/accounts')

app.register_blueprint(accounts_api, url_prefix=main_api_url+'/accounts')


@app.route('/')
def application():
    return 'Welcome to the Neo Sports application!'
