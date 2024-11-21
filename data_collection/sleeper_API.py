import requests
import pandas as pd
import time

__all__ = ['fetch_all_players', 'get_league_info', 'get_league_rosters', 'get_league_users',
           'get_league_matchups', 'get_league_playoff_brackets', 'get_league_transactions', 'get_nfl_state',
           'get_league_traded_picks', 'get_user_drafts', 'get_league_drafts', 'get_draft',
           'get_draft_picks', 'get_traded_draft_picks', 'get_trending_players']

API_calls_per_minute = 1000

def fetch_all_players():
    print(f'WARNING: Only do this max once per day!')

    start_time = time.time()

    url = f'https://api.sleeper.app/v1/players/nfl'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        players_data = response.json()
        return players_data
    else:
        print()
        print(f'Failed to retrieve league data: {response.status_code}')


def get_league_info(league_id='1095093570517798912'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        league_data = response.json()
        return league_data
    else:
        print()
        print(f'Failed to retrieve league data: {response.status_code}')


def get_league_rosters(league_id='1095093570517798912'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/rosters'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        league_data = response.json()
        return league_data
    else:
        print()
        print(f'Failed to retrieve roster data: {response.status_code}')


def get_league_users(league_id='1095093570517798912'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/users'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        league_data = response.json()
        return league_data
    else:
        print()
        print(f'Failed to retrieve user data: {response.status_code}')


def get_user_leagues(user_id='474988809218420736', year=2024):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        league_data = response.json()
        return league_data
    else:
        print()
        print(f'Failed to retrieve user data: {response.status_code}')

def get_league_matchups(league_id='1095093570517798912', week=1):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/matchups/{week}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        matchup_data = response.json()
        return matchup_data
    else:
        print()
        print(f'Failed to retrieve matchup data: {response.status_code}')

def get_league_playoff_brackets(league_id='1095093570517798912'):
    start_time = time.time()

    url_winners = f'https://api.sleeper.app/v1/league/{league_id}/winners_bracket'
    url_losers  = f'https://api.sleeper.app/v1/league/{league_id}/losers_bracket'
    
    response_winners = requests.get(url_winners)
    response_losers = requests.get(url_losers)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    failed = False
    if response_winners.status_code != 200:
        print()
        print(f'Failed to retrieve winners bracket data: {response_winners.status_code}')
        failed = True  
    if response_losers.status_code != 200:
        print()
        print(f'Failed to retrieve losers bracket data: {response_losers.status_code}')
        failed = True
    
    if not failed:
        winners_bracket_data = response_winners.json()
        losers_bracket_data = response_losers.json()
        return winners_bracket_data, losers_bracket_data
    
def get_league_transactions(league_id='1095093570517798912', round=1):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/transactions/{round}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        transaction_data = response.json()
        return transaction_data
    else:
        print()
        print(f'Failed to retrieve transaction data: {response.status_code}')
    
def get_nfl_state(sport='nfl'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/state/{sport}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        state_data = response.json()
        return state_data
    else:
        print()
        print(f'Failed to retrieve matchup data: {response.status_code}')
    
def get_league_traded_picks(league_id='1095093570517798912'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/traded_picks'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        traded_picks_data = response.json()
        return traded_picks_data
    else:
        print()
        print(f'Failed to retrieve traded picks data: {response.status_code}')
    
def get_user_drafts(user_id='', year=2024):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/user/{user_id}/drafts/nfl/{year}'
    
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        traded_picks_data = response.json()
        return traded_picks_data
    else:
        print()
        print(f'Failed to retrieve user draft data: {response.status_code}')

def get_league_drafts(league_id='1095093570517798912', year=2024):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/drafts'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        draft_data = response.json()
        return draft_data
    else:
        print()
        print(f'Failed to retrieve league draft data: {response.status_code}')

def get_draft(draft_id=''):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/draft/{draft_id}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        draft_data = response.json()
        return draft_data
    else:
        print()
        print(f'Failed to retrieve draft data: {response.status_code}')

def get_draft_picks(draft_id=''):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/draft/{draft_id}/picks'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        draft_pick_data = response.json()
        return draft_pick_data
    else:
        print()
        print(f'Failed to retrieve draft pick data: {response.status_code}')

def get_traded_draft_picks(draft_id=''):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/draft/{draft_id}/traded_picks'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        traded_pick_data = response.json()
        return traded_pick_data
    else:
        print()
        print(f'Failed to retrieve traded draft pick data: {response.status_code}')


def get_trending_players(type='add', lookback_hours=24, limit=25):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/players/nfl/trending/{type}?lookback_hours={lookback_hours}&limit={limit}'
    response = requests.get(url)

    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        player_trends_data = response.json()
        return player_trends_data
    else:
        print()
        print(f'Failed to retrieve player trends data: {response.status_code}')