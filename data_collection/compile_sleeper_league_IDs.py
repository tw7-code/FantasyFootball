import sleeper_API as sleeper
import pandas as pd
import os
import json
import matplotlib.pyplot as plt 

import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

def get_league_IDs(initial_league_id='1095093570517798912'):
    # Initialize plot
    plt.ion()  # Turn on interactive mode
    _, ax = plt.subplots()
    ax.plot([], [], 'o-', label='Dynamic Points')  # Initial empty scatter plot
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.title('Dynamic Plot of X vs Y')
    plt.grid(True)

    # Load the saved queue data to pick up where last left off
    save_file_name = 'data/fantasy_leagues/sleeper_leagues.csv'
    queue_save_file_name = 'data/fantasy_leagues/sleeper_leagues_queue.json'
    if os.path.exists(save_file_name) and os.path.exists(queue_save_file_name):
        with open(save_file_name, 'r') as f:
            league_data = pd.read_csv(save_file_name)
        with open(queue_save_file_name, 'r') as f:
            queue_data = json.load(f)
            league_queue = queue_data['league_queue']
            user_queue = queue_data['user_queue']
            users_queried = queue_data['users_queried']
    else:
        league_data = pd.DataFrame()
        league_queue = {initial_league_id: sleeper.get_league_info(initial_league_id)}
        user_queue = []
        users_queried = []

    while (len(league_queue) > 0 or len(user_queue) > 0):
        # Go through all queued leagues and get set of users

        # Cycle through each queued league to get set of unique users
        current_query_count = 0
        current_query_total = len(league_queue)
        original_user_queue_length = len(user_queue)
        while len(league_queue) > 0:
            # Pop from the leageu queue and print status update
            league_id = next(iter(league_queue))
            current_query_count += 1
            league_data = pd.concat([league_data, pd.json_normalize(league_queue.pop(league_id)).convert_dtypes()], ignore_index=True)
            # Query sleeper API for all users in each league
            try:
                league_users = sleeper.get_league_users(league_id)
                league_users = [user['user_id'] for user in league_users]
                user_queue.extend(league_users)
            except Exception as e:
                print(f' | Error: {e}')
                continue
            print(f'\r  Processing League Queue | Progress: {current_query_count:,}/{current_query_total:,} | Users Found: {len(user_queue)-original_user_queue_length:,}', end='', flush=True)
        user_queue = list(set(user_queue))
        print()
        print(f'Total Users Queued: {len(user_queue):,}')

        # Save progress every cycle no matter the time stamp
        save_progress(league_data, league_queue, users_queried, user_queue)
        update_plot(ax, len(league_data), len(user_queue))

        # Cycle through queued users to find new unique leagues
        current_query_count = 0
        current_query_total = len(user_queue)
        while len(league_queue) < 1000 and len(user_queue) > 0:
            # Pop from the user queue and print status update
            user_id = user_queue.pop(0)
            users_queried.append(user_id)
            current_query_count += 1
            # Connect to sleeper API to get al leagues for the user
            try:
                user_leagues = sleeper.get_user_leagues(user_id)
                user_leagues = {
                    league['league_id']: league
                    for league in user_leagues
                    if int(league['league_id']) not in list(map(int, league_data.league_id.values))
                }
                league_queue.update(user_leagues)
            except Exception as e:
                print(f' | Error: {e}')
            print(f'\r  Processing User Queue | Progress: {current_query_count:,}/{current_query_total:,} | Unique Leagues Found: {len(league_queue):,}', end='', flush=True)
        print()
        print(f' Leagues Queued: {len(league_queue):,}')

    return league_data, league_queue, users_queried, user_queue


def save_progress(league_data, league_queue, users_queried, user_queue):
    # Create Data folder if it does not exist
    if not os.path.exists('data/fantasy_leagues/'):
        os.makedirs('data/fantasy_leagues/')
    league_data = league_data.drop(columns=[col for col in league_data.columns if col.startswith('Unnamed')])
    league_data.to_csv('data/fantasy_leagues/sleeper_leagues.csv')
    queue_dict = {'league_queue': league_queue, 'users_queried': users_queried, 'user_queue': user_queue}
    with open('data/fantasy_leagues/sleeper_leagues_queue.json', 'w') as f:
        json.dump(queue_dict, f)
    print()
    print(f'Saved Progress | {len(league_data):,} Leagues Captured')
    print()


# Function to update the plot with the newest data point
def update_plot(ax, new_x, new_y):
    # Get current data from the plot
    line = ax.lines[0] if ax.lines else None
    if line:
        x_data = list(line.get_xdata())
        y_data = list(line.get_ydata())
    else:
        x_data = []
        y_data = []
    # Append new data point
    x_data.append(new_x)
    y_data.append(new_y)

    # Calculate the slope of the last two points
    if len(x_data) > 1:
        # Get the last two points
        x1, y1 = x_data[-2], y_data[-2]
        x2, y2 = x_data[-1], y_data[-1]
        
        # Calculate slope (dy/dx)
        slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 0  # Avoid division by zero
        
        # Format the slope for display
        slope_text = f"{slope:.2f} New Users Found/League Captured"
    else:
        slope_text = ""  # Not enough points to calculate slope

    # Clear and re-plot the updated data
    ax.clear()
    ax.plot(x_data, y_data, 'o-', label='League ID Gathering Status')
    plt.xlabel('Leagues Captured')
    plt.ylabel('User IDs Queued')
    plt.title('Leagues Captured vs. User ID Queue Size')
    plt.grid(True)
    ax.set_xlim(left=0)
    ax.legend([slope_text], loc='best')  # Add slope info to the legend
    plt.draw()
    plt.pause(1)  # Pause to allow the plot to update


if __name__ == "__main__":
    leagues = get_league_IDs()
    
