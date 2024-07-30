import requests
from dotenv import load_dotenv
import os
from datetime import datetime

__all__ = ['get_news', 'get_game_info', 'get_scores', 'get_weekly_schedule',
           'get_team_schedule', 'get_gameday_schedule', 'get_box_score', 'get_fantasy_projections',
           'get_team_stats', 'get_ADP_data', 'get_player_info', 'get_player_stats',
           'get_betting_odds', 'get_team_roster', 'get_player_list']

def get_headers_and_host():

    load_dotenv()
    api_key = os.getenv('RAPID_API_KEY')
    database_url = os.getenv('RAPID_DATABASE_URL')    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": database_url
    }
    return headers


def get_news(playerID, teamID, teamAbv, topNews, fantasyNews, recentNews, maxItems):
    
    database_name = 'getNFLNews'

    querystring = {
        "playerID": str(playerID),
        "teamID": str(teamID),
        "teamAbv": str(teamAbv),
        "topNews": str(topNews),
        "fantasyNews": str(fantasyNews),
        "recentNews": str(recentNews),
        "maxItems": str(maxItems)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_game_info(gameID):
    
    database_name = 'getNFLGameInfo'

    querystring = {
        'gameID': str(gameID)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_scores(gameDate, gameID, topPerformers, gameWeek, season, seasonType):
    
    database_name = 'getNFLScoresOnly'

    querystring = {
        "gameDate": str(gameDate),
        "gameID": str(gameID),
        "topPerformers": str(topPerformers),
        "gameWeek": str(gameWeek),
        "season": str(season),
        "seasonType": str(seasonType)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_weekly_schedule(week, seasonType, season):
    
    database_name = 'getNFLGamesForWeek'

    querystring = {
        "week": str(week),
        "seasonType": str(seasonType),
        "season": str(season)
    } 
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_team_schedule(teamID, teamAbv, season):
    
    database_name = 'getNFLTeamSchedule'

    querystring = {
        "teamID": str(teamID),
        "teamAbv": str(teamAbv),
        "season": str(season)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_gameday_schedule(gameDate):
    
    database_name = 'getNFLGamesForDate'

    querystring = {
        "gameDate": str(gameDate)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_box_score(gameID, playByPlay):
    
    database_name = 'getNFLBoxScore'

    querystring = {
        "gameID": str(gameID),
        "playByPlay": str(playByPlay)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_fantasy_projections(week, season=2024, ppr=1.0, passTD=6.0):
    
    database_name = 'getNFLProjections'

    querystring = {
        "week": str(week),
        "archiveSeason": str(season),
        "pointsPerReception": str(ppr),
        "passTD": str(passTD),
        "passAttempts": "0.0",
        "passCompletion": "0.0",
        "carries": "0.0",
        "targets": "0.0"
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_team_stats(season=2024):
    
    database_name = 'getNFLTeams'

    querystring = {
        "sortBy": "standings",
        "rosters": "true",
        "schedules": "true",
        "topPerformers": "true",
        "teamStats": "true",
        "teamStatsSeason": str(season)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_ADP_data(adp_type='PPR', adpDate='today', pos=''):
    
    database_name = 'getNFLADP'

    if adpDate == 'today':
        adpDate = datetime.today().strftime('%Y%m%d')

    querystring = {
        'adpType': str(adp_type),
        'adpDate': str(adpDate),
        'pos': str(pos)
    }

    if pos == '':
        querystring.pop('pos')

    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_player_info(playerName='', playerID='', getStats='true'):
    
    database_name = 'getNFLPlayerInfo'

    querystring = {
        "playerName": str(playerName),
        "playerID": str(playerID),
        "getStats": str(getStats)
    }

    if playerName=='':
        querystring.pop('playerName')
    if playerID=='':
        querystring.pop('playerID')

    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_player_stats(playerID='', gameID='', numberOfGames='', ppr=1.0, passTD=6.0):
    
    database_name = 'getNFLGamesForPlayer'

    querystring = {
        "playerID": str(playerID),
        "gameID": str(gameID),
        "numberOfGames": str(numberOfGames),
        "pointsPerReception": str(ppr),
        "passTD": str(passTD),
        "passAttempts": "0.0",
        "passCompletion": "0.0",
        "carries": "0.0",
        "targets": "0.0"
    }

    if playerID=='':
        querystring.pop('playerID')
    if gameID=='':
        querystring.pop('gameID')
    if numberOfGames=='':
        querystring.pop('numberOfGames')

    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_betting_odds(gameDate, gameID):
    
    database_name = 'getNFLBettingOdds'

    querystring = {
        "gameDate": str(gameDate),
        "gameID": str(gameID)
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_team_roster(teamAbv, archiveDate='today'):
    
    database_name = 'getNFLTeamRoster'

    if adpDate == 'today':
        adpDate = datetime.today().strftime('%Y%m%d')

    querystring = {
        "teamAbv": str(teamAbv),
        "archiveDate": str(archiveDate),
        "getStats": "true"
    }
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)


def get_player_list():
    
    database_name = 'getNFLPlayerList'

    querystring = {}
    headers = get_headers_and_host()
    url = f'https://{headers['x-rapidapi-host']}/{database_name}'

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        print()
        print(querystring)