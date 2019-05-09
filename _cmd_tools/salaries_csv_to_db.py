from sqlalchemy.orm import sessionmaker
from models.db_models import Player, Salary
from models.db_engine import engine
import pandas as pd


Session = sessionmaker(bind=engine)


def salaries_csv_to_db(file_path, year):
    df = pd.read_csv(file_path)
    df = df[['PLAYER', 'SALARY']]

    print(df)

    session = Session()
    data_count = len(df)

    for index, row in df.iterrows():
        player = session.query(Player.Id).filter(Player.Year == year, Player.Name == row['PLAYER']).first()

        salary = Salary()
        salary.PlayerId = player.Id
        salary.Salary = row['SALARY']

        session.add(salary)
        session.flush()

        print('Inserting players {}-{} salaries to the database ( {} / {} ) ...'
              .format(year, year+1, index + 1, data_count))

    print('DONE.')
    session.commit()
