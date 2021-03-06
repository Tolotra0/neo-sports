# Request for fetching game statistics
# Note the aliases in the two Teams tables: Team and Opponents
#
# COLUMNS FETCHED ARE:
# ['Date', 'Duration', 'Win', 'TeamFullName', 'TeamShortName',
#  'OpFullName', 'OpShortName', 'Id', 'GameId', 'FGM', 'FGA', 'TPM', 'TPA',
#  'FTM', 'FTA', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'TF', 'PTS',
#  'GameType', 'LocationType', 'TeamConference', 'OppConference']
#
base_game_request = 'SELECT Games.Date, Games.Duration, Games.Win, Team.FullName AS TeamFullName, '\
                'Team.ShortName AS TeamShortName, Team.Id as TeamId, Opponent.FullName AS OpFullName, '\
                'Opponent.ShortName AS OpShortName, TeamGameStats.*, '\
                'GameTypes.Type AS GameType, GameLocationTypes.LocationType, ' \
                'TeamConf.Name AS TeamConference, OppConf.Name AS OppConference FROM Games '\
                \
                'JOIN Teams Team JOIN Cities TeamCity JOIN Divisions TeamDiv JOIN Conferences TeamConf '\
                'ON Games.TeamId = Team.Id AND Team.CityId = TeamCity.Id AND TeamCity.DivisionId = TeamDiv.Id ' \
                'AND TeamDiv.ConferenceId = TeamConf.Id '\
                \
                'JOIN Teams Opponent JOIN Cities OppCity JOIN Divisions OppDiv JOIN Conferences OppConf '\
                'ON Opponent.Id = Games.OpponentId AND Opponent.CityId = OppCity.Id ' \
                'AND OppCity.DivisionId = OppDiv.Id AND OppDiv.ConferenceId = OppConf.Id ' \
                \
                'JOIN TeamGameStats ON Games.Id = TeamGameStats.GameId '\
                'JOIN GameTypes ON Games.GameTypeId = GameTypes.Id '\
                'JOIN GameLocationTypes ON Games.GameLocationTypeId = GameLocationTypes.Id ' \
                    '' \
                    'WHERE (ISNULL(:team) OR Team.ShortName = :team) ' \
                    'AND (ISNULL(:year) OR YEAR(Games.Date) = :year) ' \
                    'AND (ISNULL(:month) OR MONTH(Games.Date) = :month) ' \
                    'AND (ISNULL(:day) OR DAY(Games.Date) = :day) ' \
                    'AND (ISNULL(:conference) OR TeamConf.Name = :conference) ' \

# Filter game results to an one season result
season_filter = ' ((YEAR(Games.Date) = :beginYear AND MONTH(Games.Date) >= :beginMonth) \
                OR (YEAR(Games.Date) = :endYear AND MONTH(Games.Date) <= :endMonth)) '

# Basic sorting for all games stats results
sorting = ' ORDER BY Team.FullName, Games.Date '


# Season parameters
season_start_month = 10
season_end_month = 8

# Stats used for data visualization
visualization_columns = ['FGM', 'FGA', 'TPM', 'TPA', 'FTM', 'FTA', 'OREB',
                         'DREB', 'AST', 'TOV', 'STL', 'BLK', 'TF', 'PTS']


# Requests for fetching players
#
# Columns fetched are
player_request = 'SELECT Players.Year, Players.Name, Players.Age, ' \
                 'Teams.Id AS TeamId, Teams.FullName AS TeamFullName, Teams.ShortName AS TeamAbbr, ' \
                 'PlayerStats.*, GameTypes.Type AS GameType, Salaries.Salary ' \
                 'FROM Players ' \
                 \
                 'JOIN PlayerStats JOIN GameTypes ' \
                 'ON PlayerStats.PlayerId = Players.Id AND PlayerStats.GameTypeId = GameTypes.Id ' \
                 \
                 'JOIN Teams on Teams.Id = Players.TeamId ' \
                 \
                 'LEFT JOIN Salaries ON Players.Id = Salaries.PlayerId ' \
                 \
                 'WHERE ( ISNULL(:name) OR INSTR(Players.Name, :name) ) ' \
                 'AND ( ISNULL(:year) OR Players.Year = :year ) ' \
                 'AND ( ISNULL(:age) OR Players.Age = :age ) ' \
                 'AND ( ISNULL(:team) OR Teams.ShortName = :team ) ' \
                 'AND ( ISNULL(:game_type) OR INSTR(GameTypes.Type, :game_type) ) ' \
                 'AND ( ISNULL(:id) OR Players.Id = :id )' \
                 'ORDER BY Players.Year, Players.Name'

# Stats used for player data visualization
player_visualization_columns = ['Age', 'GP', 'W', 'L', 'MIN',
                                'FGM', 'FGA', 'TPM', 'TPA', 'FTM', 'FTA', 'OREB',
                                'DREB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'PTS',
                                'DD2', 'TD3']
