import requests
import pandas as pd

def fetch_sleeper_players():
    # URL for Sleeper API to get all players
    url = 'https://api.sleeper.app/v1/players/nfl'
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    # Parse the JSON response
    players_data = response.json()
    
    # Convert the JSON data to a pandas DataFrame
    df = pd.DataFrame.from_dict(players_data, orient='index')
    
    return df

if __name__ == "__main__":
    player_df = fetch_sleeper_players()
    print(player_df)