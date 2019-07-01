from flask import Blueprint, jsonify, request
import pandas as pd
import pickle
import json


prediction_api = Blueprint('prediction_api', __name__)


game_model_path = './prediction/my_pipeline.pkl'



@prediction_api.route('/game', methods=['POST'])
def game_pred():

    data = json.loads(request.data)
    df = pd.DataFrame([{
        'TeamId': data['TeamId'],
        'AST': data['AST'],
        'STL': data['STL'],
        'TF': data['TF'],
        'BLK': data['BLK'],
        'TOV': data['TOV'],
        'OREB': data['OREB'],
        'TREB': data['TREB'],
        'FGM': data['FGM'],
        'FGA': data['FGA'],
        'FTM': data['FTM'],
        'FTA': data['FTA'],
        'PTS': data['PTS']
    }])
    row = [df.iloc[0]]

    print(row)

    model = None

    with (open(game_model_path, 'rb')) as opened_model:
        model = pickle.load(opened_model)

    print(model)

    result = model.predict(row)

    print(result)

    return jsonify({'win_prob': result[0], 'mae': 0.288})
