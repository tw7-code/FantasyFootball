import sleeper_API as sleeper
import pandas as pd
import os
import json
import matplotlib.pyplot as plt 
import time
import boto3
from botocore.config import Config

import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

def get_league_IDs(initial_league_id='1095093570517798912', leagues_per_cycle=1000, plot_bool=False):
    """
    Retrieves and processes league IDs from the Sleeper fantasy football platform.

    This function initializes a dynamic visualization of the data retrieval process
    and iteratively queries Sleeper's API to discover unique leagues and their associated
    users. It maintains progress across sessions by saving and loading data, and dynamically
    updates plots showing the current state of the data acquisition.

    Parameters:
        initial_league_id (str): The ID of the starting league to begin data collection. 
            - Defaults to '1095093570517798912'.

    Returns:
        tuple: A tuple containing:
            - league_data (pandas.DataFrame): A dataframe containing all retrieved league information.
            - league_queue (dict): A dictionary of leagues queued for processing.
            - users_queried (list): A list of user IDs that have been queried.
            - user_queue (list): A list of user IDs still queued for querying.
    """
    session = boto3.Session(profile_name='tw7')
    s3 = session.client('s3')
    download_files_from_s3(s3, 'tw7-bucket-ffb', 'fantasy_leagues', 'data')
    
    if plot_bool:
        ax1, ax2 = initialize_plot()

    last_save_time = time.time()

    # Initialize the function to pick up where it left off
    league_data_csv = os.path.join('data', 'fantasy_leagues', 'sleeper_leagues.csv')
    queue_csv = os.path.join('data', 'fantasy_leagues', 'sleeper_leagues_queue.json')
    league_data, league_queue, users_queried, user_queue = initialize_league_query(league_data_csv, queue_csv, initial_league_id)

    while (len(league_queue) > 0 or len(user_queue) > 0):
        # Process queues
        user_queue, users_queried, league_queue, league_data = search_user_queue(user_queue, users_queried, league_queue, league_data, leagues_per_cycle)
        user_queue, users_queried, league_queue, league_data = search_league_queue(user_queue, users_queried, league_queue, league_data)

        # Save progress every cycle
        last_save_time, lpm = save_progress(last_save_time, league_data, league_queue, users_queried, user_queue)
        upload_directory_to_s3(s3, 'tw7-bucket-ffb', 'fantasy_leagues')
        
        # Update plots
        if plot_bool:
            update_plot(ax1, ax2, len(league_data), len(user_queue), lpm)

def initialize_league_query(league_data_csv, queue_csv, initial_league_id):
    # Load the saved queue data to pick up where last left off
    if os.path.exists(league_data_csv) and os.path.exists(queue_csv):
        with open(league_data_csv, 'r') as f:
            league_data = pd.read_csv(league_data_csv, low_memory=False)
        with open(queue_csv, 'r') as f:
            queue_data = json.load(f)
            league_queue = queue_data['league_queue']
            user_queue = queue_data['user_queue']
            users_queried = queue_data['users_queried']
    else:
        league_data = pd.DataFrame()
        league_queue = {initial_league_id: sleeper.get_league_info(initial_league_id)}
        user_queue = []
        users_queried = []
        
    return league_data, league_queue, users_queried, user_queue

def search_user_queue(user_queue, users_queried, league_queue, league_data, leagues_per_cycle):
    # Cycle through queued users to find new unique leagues
    current_query_count = 0
    current_query_total = len(user_queue)
    while len(league_queue) < leagues_per_cycle and len(user_queue) > 0:
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
            print()
            print(f'League Processing Error: {e}')
            continue
        print(f'\rProcessing User Queue | Progress: {current_query_count:,}/{current_query_total:,} | Unique Leagues Found: {len(league_queue):,}', end='', flush=True)
    print()
    print(f'Leagues Queued: {len(league_queue):,}')
    
    return user_queue, users_queried, league_queue, league_data

def search_league_queue(user_queue, users_queried, league_queue, league_data):
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
            print()
            print(f'User Processing Error: {e}')
            continue
        print(f'\rProcessing League Queue | Progress: {current_query_count:,}/{current_query_total:,} | Total Users in Leagues: {len(user_queue)-original_user_queue_length:,} | Total League Count: {len(league_data):,}', end='', flush=True)
    user_queue = list(set(user_queue))
    print()
    print(f'Total Users Queued: {len(user_queue):,} | Unique Users Added: {len(user_queue)-original_user_queue_length:,} | Total Users Discovered: {len(user_queue) + len(users_queried):,}')
    
    return user_queue, users_queried, league_queue, league_data

def save_progress(last_save_time, league_data, league_queue, users_queried, user_queue):
    """
    Saves the current progress of league and user data retrieval to disk.

    This function ensures that progress is preserved by saving the league data
    and the current state of the queues to disk in a structured format. It also
    logs the number of leagues captured and calculates the rate of league processing.

    Parameters:
        last_save_time (float): The timestamp of the last save operation.
        league_data (pandas.DataFrame): A dataframe containing all retrieved league information.
        league_queue (dict): A dictionary of leagues queued for processing.
        users_queried (list): A list of user IDs that have been queried.
        user_queue (list): A list of user IDs still queued for querying.

    Returns:
        tuple: A tuple containing:
            - current_time (float): The updated timestamp of the save operation.
            - processing_rate (float): The calculated rate of leagues processed per minute since the last save.
    """
    # Create Data folder if it does not exist
    directory = os.path.join('data', 'fantasy_leagues')
    league_data_file = os.path.join(directory, 'sleeper_leagues.csv')
    queue_data_file = os.path.join(directory, 'sleeper_leagues_queue.json')
    if not os.path.exists(directory):
        os.makedirs(directory)
    league_data = league_data.drop(columns=[col for col in league_data.columns if col.startswith('Unnamed')])
    league_data.to_csv(league_data_file)
    queue_dict = {'league_queue': league_queue, 'users_queried': users_queried, 'user_queue': user_queue}
    with open(queue_data_file, 'w') as f:
        json.dump(queue_dict, f)
    time_since_last_save = (time.time() - last_save_time) / 60 # in minutes
    print()
    print(f'Saved Progress | {len(league_data):,} Leagues Captured')
    print(f'Time since last save: {time_since_last_save:.2f} minutes | {1000 / time_since_last_save:.2f} Leagues/min')
    print()
    return time.time(), 1000 / time_since_last_save

def upload_directory_to_s3(s3, bucket_name, local_directory):
    """
    Uploads a directory and its contents to an S3 bucket, preserving the full folder structure as S3 prefixes.

    Args:
        s3 (boto3.client): An initialized S3 client.
        bucket_name (str): Name of the S3 bucket.
        local_directory (str): Path to the local base directory to upload.
    """
    print('Uploading Files to S3:')
    try:
        for root, _, files in os.walk(local_directory):
            for file in files:
                # Construct full local file path
                local_file_path = os.path.join(root, file)

                # Use os.path.relpath for relative paths to ensure portability
                s3_file_key = os.path.relpath(local_file_path, local_directory).replace(os.sep, "/")
                
                # Upload the file
                s3.upload_file(local_file_path, bucket_name, s3_file_key)
                print(f"  Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_key}")
    except Exception as e:
        print(f"Error uploading directory: {e}")
        
def download_files_from_s3(s3, bucket_name, s3_prefix, local_directory):
    """
    Downloads all files from an S3 prefix and saves them into a specified local directory,
    preserving the prefix and filenames.

    Args:
        s3 (boto3.client): An initialized S3 client.
        bucket_name (str): Name of the S3 bucket.
        s3_prefix (str): The prefix (folder structure) in the S3 bucket.
        local_directory (str): Local directory to save the files.
    """
    print('Downloading Files from S3:')
    try:
        # Normalize the base local directory path
        base_local_directory = os.path.normpath(os.path.join(local_directory, s3_prefix.strip('/').replace("/", "_")))
        os.makedirs(base_local_directory, exist_ok=True)

        # List all objects under the given prefix
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)

        if 'Contents' not in response:
            print(f"No files found under prefix '{s3_prefix}' in bucket '{bucket_name}'.")
            return

        # Download all files
        for obj in response['Contents']:
            s3_file_key = obj['Key']

            # Use relative paths and normalize them for the local system
            relative_path = os.path.normpath(s3_file_key[len(s3_prefix):].lstrip('/'))
            local_file_path = os.path.normpath(os.path.join(base_local_directory, relative_path))

            # Ensure local directories exist
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download the file
            s3.download_file(bucket_name, s3_file_key, local_file_path)
            print(f"  Downloaded {s3_file_key} to {local_file_path}")
    
    except Exception as e:
        print(f"Error downloading files: {e}")

def initialize_plot():
    # Initialize plot
    plt.ion()  # Turn on interactive mode
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 13))  # Create two vertically stacked subplots
    ax1.plot([], [], 'o-', label='User Queue Points')  # Initial empty scatter plot
    ax1.grid(True)
    ax2.plot([], [], 'o-', label='LPM Points', color='orange')  # Initial empty scatter plot
    ax2.grid(True)
    
    return ax1, ax2

def update_plot(ax1, ax2, new_x, new_y, lpm):
    """
    Updates the dynamic plots for league and user data retrieval progress.

    This function updates two plots:
    1. A plot showing the number of user IDs queued versus leagues captured.
    2. A plot monitoring the rate of league capture (leagues per minute).

    It recalculates the data, clears the plots, and redraws them with the latest information.

    Parameters:
        ax1 (matplotlib.axes.Axes): The first subplot for league-to-user data visualization.
        ax2 (matplotlib.axes.Axes): The second subplot for monitoring leagues captured per minute.
        new_x (int): The current number of leagues captured.
        new_y (int): The current size of the user ID queue.
        lpm (float): The calculated leagues per minute processing rate.

    Returns:
        None
    """
    # Update main chart (ax1)
    line1 = ax1.lines[0] if ax1.lines else None
    if line1:
        x_data1 = list(line1.get_xdata())
        y_data1 = list(line1.get_ydata())
    else:
        x_data1 = []
        y_data1 = []
    # Append new data point
    x_data1.append(new_x)
    y_data1.append(new_y)

    # Calculate the slope for ax1
    if len(x_data1) > 1:
        x1, y1 = x_data1[-2], y_data1[-2]
        x2, y2 = x_data1[-1], y_data1[-1]
        slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        slope_text1 = f"{slope1:.2f} New Users Found/League Captured"
    else:
        slope_text1 = ""

    # Clear and re-plot ax1
    ax1.clear()
    ax1.plot(x_data1, y_data1, 'o-', label='League ID Gathering Status')
    ax1.set_xlabel('Leagues Captured')
    ax1.set_ylabel('User IDs Queued')
    ax1.set_title('Leagues Captured vs. User ID Queue Size')
    ax1.grid(True)
    ax1.legend([slope_text1], loc='best')

    # Update subplot for lpm (ax2)
    line2 = ax2.lines[0] if ax2.lines else None
    if line2:
        x_data2 = list(line2.get_xdata())
        y_data2 = list(line2.get_ydata())
    else:
        x_data2 = []
        y_data2 = []

    # Append new lpm data point
    x_data2.append(new_x)
    y_data2.append(lpm)

    # Clear and re-plot ax2
    ax2.clear()
    ax2.plot(x_data2, y_data2, 'o-', label='Leagues Found per Minute', color='orange')
    ax2.set_xlabel('Total Leagues Captured')
    ax2.set_ylabel('Leagues/Minute')
    ax2.set_title('League Capture Rate Monitor')
    ax2.grid(True)

    # Update the plots
    plt.draw()
    plt.pause(1)
    
def clean_sleeper_league_data(league_data):
    pass

if __name__ == "__main__":
    get_league_IDs(leagues_per_cycle=5000)
    