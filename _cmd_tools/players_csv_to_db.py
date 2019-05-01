from sqlalchemy.orm import sessionmaker
from models.db_models import PlayerStat, Player
from models.db_engine import engine
import pandas as pd


Session = sessionmaker(bind=engine)


# Assuming that the CSV contains these columns:
# ['PLAYER', 'TEAM', 'AGE', 'GP', 'W', 'L', 'MIN', 'PTS',
# 'FGM', 'FGA', 'TPA', 'TPM', 'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'TOV',
# 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', '+/-']
# And all these columns doesn't contain strings


def players_csv_to_db(file_path, year, game_type):
    df = pd.read_csv(file_path)

    session = Session()
    data_count = len(df)

    for index, row in df.iterrows():
        player = generate_player_class(row, year)

        session.add(player)
        session.flush()

        stats = generate_player_stat_class(row, game_type)
        stats.PlayerId = player.Id

        session.add(stats)
        session.flush()

        print('Inserting player stats to the database ( {} / {} ) ...'.format(index + 1, data_count))

    session.commit()
    print('DONE.')


def generate_player_stat_class(row, game_type):
    stats = PlayerStat()

    stats.GP = row['GP']
    stats.W = row['W']
    stats.L = row['L']
    stats.MIN = row['MIN']
    stats.PTS = row['PTS']
    stats.FGM = row['FGM']
    stats.FGA = row['FGA']
    stats.TPA = row['TPA']
    stats.TPM = row['TPM']
    stats.FTM = row['FTM']
    stats.FTA = row['FTA']
    stats.OREB = row['OREB']
    stats.DREB = row['DREB']
    stats.AST = row['AST']
    stats.TOV = row['TOV']
    stats.STL = row['STL']
    stats.BLK = row['BLK']
    stats.PF = row['PF']
    stats.FP = row['FP']
    stats.DD2 = row['DD2']
    stats.TD3 = row['TD3']
    stats.PlusMinus = row['+/-']

    stats.GameTypeId = game_type

    return stats


def generate_player_class(row, year):
    player = Player()

    player.Name = row['PLAYER']
    player.TeamId = row['TEAM']
    player.Age = row['AGE']
    player.Year = year

    return player
