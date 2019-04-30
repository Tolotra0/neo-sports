from sqlalchemy.orm import sessionmaker
from models.db_models import Game, TeamGameStat
from models.db_engine import engine
import pandas as pd
import datetime


Session = sessionmaker(bind=engine)


# Assuming that the CSV contains these columns:
# ['TeamId', 'Game', 'Date', 'GameLocationTypeId', 'OpponentId', 'Win',
#  'PTS', 'FGM', 'FGA', 'TPM', 'TPA', 'FTM', 'FTA', 'OREB', 'TREB', 'AST',
#  'STL', 'BLK', 'TOV', 'TF']
# And all these columns doesn't contain strings

def game_csv_to_db(csv_file_path):
    print('')

    df = pd.read_csv(csv_file_path)
    df['DREB'] = df['TREB'] - df['OREB']

    session = Session()

    data_count = len(df)

    for index, row in df.iterrows():
        game = _generate_game_class(row)

        session.add(game)
        session.flush()

        game_stats = _generate_game_stats_class(row)
        game_stats.GameId = game.Id

        session.add(game_stats)
        session.flush()

        print('Inserting game stats to the database ( {} / {} ) ...' .format(index + 1, data_count))

    session.commit()
    print('DONE.')


def _generate_game_class(row):
    game = Game()
    game.Date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d')
    game.Duration = None
    game.TeamId = row['TeamId']
    game.OpponentId = row['OpponentId']

    if 'GameTypeId' in row:
        game.GameTypeId = row['GameTypeId']
    else:
        game.GameTypeId = 1

    game.GameLocationTypeId = row['GameLocationTypeId']
    game.Win = row['Win']

    return game


def _generate_game_stats_class(row):
    team_game_stat = TeamGameStat()

    team_game_stat.PTS = row['PTS']
    team_game_stat.FGM = row['FGM']
    team_game_stat.FGA = row['FGA']
    team_game_stat.TPM = row['TPM']
    team_game_stat.TPA = row['TPA']
    team_game_stat.FTM = row['FTM']
    team_game_stat.FTA = row['FTA']
    team_game_stat.OREB = row['OREB']
    team_game_stat.DREB = row['DREB']
    team_game_stat.AST = row['AST']
    team_game_stat.STL = row['STL']
    team_game_stat.BLK = row['BLK']
    team_game_stat.TOV = row['TOV']
    team_game_stat.TF = row['TF']

    return team_game_stat
