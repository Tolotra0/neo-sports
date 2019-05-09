# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'Admins'

    Id = Column(INTEGER(11), primary_key=True)
    Username = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)


class BasketballPosition(Base):
    __tablename__ = 'BasketballPositions'

    Id = Column(INTEGER(4), primary_key=True)
    FullName = Column(String(255), nullable=False)
    ShortName = Column(String(4), nullable=False)


class Conference(Base):
    __tablename__ = 'Conferences'

    Id = Column(INTEGER(4), primary_key=True)
    Name = Column(String(255), nullable=False)


class GameLocationType(Base):
    __tablename__ = 'GameLocationTypes'

    Id = Column(INTEGER(4), primary_key=True)
    LocationType = Column(String(255), nullable=False)


class GameType(Base):
    __tablename__ = 'GameTypes'

    Id = Column(INTEGER(4), primary_key=True)
    Type = Column(String(255), nullable=False)


class Division(Base):
    __tablename__ = 'Divisions'

    Id = Column(INTEGER(4), primary_key=True)
    Name = Column(String(255), nullable=False)
    ConferenceId = Column(ForeignKey('Conferences.Id'), nullable=False, index=True)

    Conference = relationship('Conference')


class City(Base):
    __tablename__ = 'Cities'

    Id = Column(INTEGER(4), primary_key=True)
    Name = Column(String(255), nullable=False)
    DivisionId = Column(ForeignKey('Divisions.Id'), nullable=False, index=True)

    Division = relationship('Division')


class Team(Base):
    __tablename__ = 'Teams'

    Id = Column(INTEGER(4), primary_key=True)
    FullName = Column(String(255), nullable=False)
    ShortName = Column(String(3), nullable=False)
    ShortNameAlt = Column(String(3))
    CityId = Column(ForeignKey('Cities.Id'), index=True)

    City = relationship('City')


class Game(Base):
    __tablename__ = 'Games'

    Id = Column(INTEGER(16), primary_key=True)
    Date = Column(Date, nullable=False)
    Duration = Column(Float)
    TeamId = Column(ForeignKey('Teams.Id'), nullable=False, index=True)
    OpponentId = Column(ForeignKey('Teams.Id'), nullable=False, index=True)
    GameTypeId = Column(ForeignKey('GameTypes.Id'), nullable=False, index=True)
    GameLocationTypeId = Column(ForeignKey('GameLocationTypes.Id'), index=True)
    Win = Column(INTEGER(4), nullable=False)

    GameLocationType = relationship('GameLocationType')
    GameType = relationship('GameType')
    Team = relationship('Team', primaryjoin='Game.OpponentId == Team.Id')
    Team1 = relationship('Team', primaryjoin='Game.TeamId == Team.Id')


class Player(Base):
    __tablename__ = 'Players'

    Id = Column(INTEGER(16), primary_key=True)
    Year = Column(INTEGER(4), nullable=False)
    Name = Column(String(255), nullable=False)
    Age = Column(INTEGER(4), nullable=False)
    Height = Column(Float)
    Weight = Column(Float)
    BirthDate = Column(Date)
    MainPositionId = Column(ForeignKey('BasketballPositions.Id'), index=True)
    SecondPostionId = Column(ForeignKey('BasketballPositions.Id'), index=True)
    TeamId = Column(ForeignKey('Teams.Id'), index=True)

    BasketballPosition = relationship('BasketballPosition', primaryjoin='Player.MainPositionId == BasketballPosition.Id')
    BasketballPosition1 = relationship('BasketballPosition', primaryjoin='Player.SecondPostionId == BasketballPosition.Id')
    Team = relationship('Team')


class PlayerStat(Base):
    __tablename__ = 'PlayerStats'

    Id = Column(INTEGER(16), primary_key=True)
    PlayerId = Column(ForeignKey('Players.Id'), nullable=False, index=True)
    GameTypeId = Column(ForeignKey('GameTypes.Id'), nullable=False, index=True)
    GP = Column(INTEGER(10), nullable=False)
    W = Column(INTEGER(10), nullable=False)
    L = Column(INTEGER(10), nullable=False)
    MIN = Column(Float, nullable=False)
    FGM = Column(Float)
    FGA = Column(Float)
    TPM = Column(Float)
    TPA = Column(Float)
    FTM = Column(Float)
    FTA = Column(Float)
    OREB = Column(Float)
    DREB = Column(Float)
    AST = Column(Float)
    TOV = Column(Float)
    STL = Column(Float)
    BLK = Column(Float)
    PF = Column(Float)
    FP = Column(Float)
    PTS = Column(Float)
    DD2 = Column(INTEGER(10), nullable=False)
    TD3 = Column(INTEGER(10), nullable=False)
    PlusMinus = Column(Float)

    GameType = relationship('GameType')
    Player = relationship('Player')


class Salary(Base):
    __tablename__ = 'Salaries'

    Id = Column(INTEGER(16), primary_key=True)
    PlayerId = Column(ForeignKey('Players.Id'), nullable=False, index=True)
    Salary = Column(INTEGER(16), nullable=False)

    Player = relationship('Player')


class TeamGameStat(Base):
    __tablename__ = 'TeamGameStats'

    Id = Column(INTEGER(16), primary_key=True)
    GameId = Column(ForeignKey('Games.Id'), nullable=False, index=True)
    FGM = Column(INTEGER(10))
    FGA = Column(INTEGER(10))
    TPM = Column(INTEGER(10))
    TPA = Column(INTEGER(10))
    FTM = Column(INTEGER(10))
    FTA = Column(INTEGER(10))
    OREB = Column(INTEGER(10))
    DREB = Column(INTEGER(10))
    AST = Column(INTEGER(10))
    TOV = Column(INTEGER(10))
    STL = Column(INTEGER(10))
    BLK = Column(INTEGER(10))
    TF = Column(INTEGER(10))
    PTS = Column(INTEGER(10))

    Game = relationship('Game')
