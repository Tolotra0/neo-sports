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
                'Team.ShortName AS TeamShortName, Opponent.FullName AS OpFullName, '\
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
                'JOIN GameLocationTypes ON Games.GameLocationTypeId = GameLocationTypes.Id '

# Filter game results to an one season result
season_filter = ' WHERE ((YEAR(Games.Date) = :beginYear AND MONTH(Games.Date) >= :beginMonth) \
                OR (YEAR(Games.Date) = :endYear AND MONTH(Games.Date) <= :endMonth)) '

# Basic sorting for all games stats results
sorting = ' ORDER BY Team.Id, Games.Date '


# Season parameters
season_start_month = 10
season_end_month = 4
