# neo-sports
A set of (intelligent) tools developed to improve the Malagasy collective sport.

## Installation
The project needs a Python 3 environment with the packages specified in the **requirements.txt**.
We mainly recommend a **Conda environment**.

- python==3.7.*
- flask==1.0.2
- sqlalchemy==1.2.15
- pymysql==0.9.3
- pandas==0.23.4
- scikit-learn==0.20.1
- flask-cors==3.0.7

Theses packages aren't required in production mode but required in development:

- matplotlib==3.0.2
- sqlacodegen==2.0.1

Also, this project uses a **MariaDB** (or MySQL) database, so install it.
The database file are stored in the **_db_backups** folder.
And the last named file is the most recent file.

## API Documentation

### Main API

#### Basic Datas

##### All games stats
For getting all the games stats stored in the database:
`/api/main/games` or `/api/main/games/all`

<br>

##### Games stats by team
For getting multiple games stats mainly filtered by **team**:

    /api/main/games/team/<TEAM_ABBR>[/<SEASON_BEGIN_YEAR>/<MONTH>/<DAY>]
    
**Strings stored in <..> are parameters, and strings stored in [..] are optionals parameters.**
- **TEAM_ABBR:** Team name abbreviation (HOU, TOR, CLE, SAC, ...).
- **SEASON_BEGIN_YEAR:** (optional) Specifies the begin year of the season. For example, 2015 means the 2015-2016 season.
- **MONTH:** (optional) Month filtering (integer value).
- **DAY:** (optional) Day filtering (integer value).

For example `/api/main/games/team/TOR/2015/1` gives us all the January games played by Toronto Raptors 
in the 2015-2016 season.

<br>

##### Games stats by season
For getting multiple games stats mainly filtered by **season**:

    /api/main/games/season/<SEASON_BEGIN_YEAR>[/<TEAM_ABBR>]
    
`/api/main/games/season/2017` gives us all the 2017-2018 season's games.

<br>

##### Season stats (aggregations)
For getting a season's games summaries. For only one season we use:

    /api/main/season/<SEASON_BEGIN_YEAR>/<AGGREGATE_METHOD>[/<CONFERENCE>]
    
- **AGGREGATE_METHOD:** `avg` or `sum`.
- **CONFERENCE:** (optional) `east` or `west`.

`/api/main/season/2014/avg` gives us the 2014-2015 season resume (AVERAGE) for all teams.
`/api/main/season/2014/avg/east` gives us the 2014-2015 season resume for the eastern conference.

For multiple season resume, we can use:

    /api/main/season/<SEASON_BEGIN_YEAR1>/to/<SEASON_BEGIN_YEAR2>/avg[/<CONFERENCE>]
    
`/api/main/season/2015/to/2017/avg` gives us one resume for the 2015-2016 till the 2017-2018 season.

For a season GLOBAL average (average of all the teams season stats):

    /api/main/season/<SEASON_BEGIN_YEAR>/global_average
    
<br>

##### Team stats
All time games resume for a team:
    
    /api/main/team/<TEAM_ABBR>/alltime/games_resume
    
Season games resume for a team:

    /api/main/team/<TEAM_ABBR>/<SEASON_BEGIN_YEAR>/games_resume
    
All time games stats average for a team:

    /api/main/team/<TEAM_ABBR>/alltime/games_stats_avg
    
Season games stats average for a team:

    /api/main/team/<TEAM_ABBR>/<SEASON_BEGIN_YEAR>/games_stats_avg
    
<br>

##### Players stats
Getting ALL the players stats (alltime):

    /api/main/players/ or /api/main/players/all
    
Getting players **by name**:

    /api/main/players/name/<NAME>[/<TEAM>/<YEAR>]
    
- **NAME** is a string that is contained in the player's full name.

Getting players **by team**:

    /api/main/players/team/<TEAM>[/<YEAR>/<GAME_TYPE>]
    
- **GAME_TYPE** is `regular` or `playoffs`

<br>

#### Machine Learning API

##### Visualization
API for getting data visualizations like points, charts, polars and so on ...

For **teams visualization with points**:

    /api/main/visualization/points/teams[/<SEASON_BEGIN_YEAR>/<CONFERENCE>]
    
<br>

##### Clustering
API for getting different sorts of clustering like teams clustering, players clustering, ...

To get **teams clustering** based on multiple parameters:

    /api/main/clustering/teams/<K>[/<SEASON_BEGIN_YEAR>/<CONFERENCE>]
    
- **K** is the number of clusters.

<br>

## MORE
The project also contain a commandline tool for adding new **structured and uniform csv** files in the database.
See the files in the **_csv_files** folder for example.

### Adding games stats in the database

    $ flask game-csv-to-db --path=<csv_file_path>
    
- **csv_file_path** is the path to the csv file.
    
### Adding player stats in the database

    $ flask players-csv-to-db --path=<csv_file_path> --game-type=<game_type> --year=<season_begin_year>
    
- **game_type:** `'Regular Season'` or `'Playoffs'`
- **season_begin_year:** The `season_begin_year - season_begin_year + 1` season.

<br><br>

_If you encounters any errors in the API or in the documentation please send a report, I'm an human being :)_

**Thanks for reading carefully.**