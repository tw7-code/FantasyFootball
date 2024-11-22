import requests
import time

__all__ = ['fetch_all_players', 'get_league_info', 'get_league_rosters', 'get_league_users',
           'get_league_matchups', 'get_league_playoff_brackets', 'get_league_transactions', 'get_nfl_state',
           'get_league_traded_picks', 'get_user_drafts', 'get_league_drafts', 'get_draft',
           'get_draft_picks', 'get_traded_draft_picks', 'get_trending_players']

def apply_API_call_delay(start_time=time.time()):
    API_calls_per_minute = 1000
    time.sleep(max(60 / API_calls_per_minute - (time.time() - start_time), 0))

def check_API_response(response):
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()

    # Handle specific error codes
    error_messages = {
        400: "Bad Request -- Your request is invalid.",
        404: "Not Found -- The specified resource could not be found.",
        429: "Too Many Requests -- You're requesting too much! Slow down!",
        500: "Internal Server Error -- We had a problem with our server. Try again later.",
        503: "Service Unavailable -- We're temporarily offline for maintenance. Please try again later."
    }

    print()
    if response.status_code in error_messages:
        print(f"Error {response.status_code}: {error_messages[response.status_code]}")
    else:
        print(f"Unexpected error: {response.status_code}")
    
    return None

def fetch_all_players():
    print('WARNING: Only do this max once per day!')
    start_time = time.time()
    url = 'https://api.sleeper.app/v1/players/nfl'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)


def get_league_info(league_id='1095093570517798912'):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/league/{league_id}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)


def get_league_rosters(league_id='1095093570517798912'):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/league/{league_id}/rosters'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)


def get_league_users(league_id='1095093570517798912'):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/league/{league_id}/users'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)


def get_user_leagues(user_id='474988809218420736', year=2024):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_league_matchups(league_id='1095093570517798912', week=1):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/league/{league_id}/matchups/{week}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_league_playoff_brackets(league_id='1095093570517798912'):
    url_winners = f'https://api.sleeper.app/v1/league/{league_id}/winners_bracket'
    url_losers  = f'https://api.sleeper.app/v1/league/{league_id}/losers_bracket'
    start_time = time.time()
    response_winners = requests.get(url_winners)
    apply_API_call_delay(start_time)
    start_time = time.time()
    response_losers = requests.get(url_losers)
    apply_API_call_delay(start_time)
    return check_API_response(response_winners), check_API_response(response_losers)
    
def get_league_transactions(league_id='1095093570517798912', round=1):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/league/{league_id}/transactions/{round}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)
    
def get_nfl_state(sport='nfl'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/state/{sport}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)
    
def get_league_traded_picks(league_id='1095093570517798912'):
    start_time = time.time()

    url = f'https://api.sleeper.app/v1/league/{league_id}/traded_picks'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)
    
def get_user_drafts(user_id='', year=2024):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/user/{user_id}/drafts/nfl/{year}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_league_drafts(league_id='1095093570517798912', year=2024):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/league/{league_id}/drafts'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_draft(draft_id=''):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/draft/{draft_id}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_draft_picks(draft_id=''):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/draft/{draft_id}/picks'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_traded_draft_picks(draft_id=''):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/draft/{draft_id}/traded_picks'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)

def get_trending_players(type='add', lookback_hours=24, limit=25):
    start_time = time.time()
    url = f'https://api.sleeper.app/v1/players/nfl/trending/{type}?lookback_hours={lookback_hours}&limit={limit}'
    response = requests.get(url)
    apply_API_call_delay(start_time)
    return check_API_response(response)