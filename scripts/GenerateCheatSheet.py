import pandas as pd
import os
import re

# Define positions
positions = ['QB', 'RB', 'WR', 'TE']

# Define the base file names

output_file = 'DynastyCheatSheet_{}.csv'

# Function to process files for each position
def redraft_vs_dynasty(position):
    # Ranking Files
    base_draft_file = './FantasyProsRankings/Redraft/FantasyPros_2024_Draft_{}_Rankings.csv'
    base_dynasty_file = './FantasyProsRankings/Dynasty/FantasyPros_2024_Dynasty_{}_Rankings.csv'

    # Load the CSV files
    draft_file = base_draft_file.format(position)
    dynasty_file = base_dynasty_file.format(position)
    
    if not os.path.exists(draft_file) or not os.path.exists(dynasty_file):
        print(f"Files for position {position} not found.")
        return

    draft_rankings = pd.read_csv(draft_file)
    dynasty_rankings = pd.read_csv(dynasty_file)

    # Merge the dataframes on the player name
    merged_df = pd.merge(dynasty_rankings, draft_rankings, on='PLAYER NAME', suffixes=('_dynasty', '_redraft'), how='left')

    # Calculate the difference between dynasty RK and redraft RK
    merged_df['RK Difference'] = merged_df['RK_redraft'] - merged_df['RK_dynasty']

    # Select the required columns
    combined_df = merged_df[['RK_dynasty', 'TIERS_dynasty', 'PLAYER NAME', 'AGE', 'TEAM_dynasty', 'RK Difference']]
    combined_df.columns = ['FPR', 'Tier', 'Name', 'Age', 'Team', 'Redraft Diff']

    return combined_df

def sleeper_adp(position):

    # Get the text from the copied file
    with open(f'./SleeperADP/Dynasty/SleeperADP_{position.upper()}.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # Define the pattern to find substrings between a newline and the position (e.g., " RB")
    pattern = rf'\n(.*?) {position}'
    # Find all substrings that match the given pattern
    matches = re.findall(pattern, text)
    
    # Create a DataFrame with the player names and their order of appearance
    df = pd.DataFrame({
        'ADP': range(1, len(matches) + 1),
        'Name': matches
    })
    
    return df

if __name__ == "__main__":
    
    for pos in positions:

        sleeper_adp_df = sleeper_adp(pos)
        sleeper_adp_df['match col'] = sleeper_adp_df['Name'].apply(lambda name: ' '.join(name.split()[:2]))
        rankings_df = redraft_vs_dynasty(pos)
        rankings_df['match col'] = rankings_df['Name'].apply(lambda name: ' '.join(name.split()[:2]))

        df = pd.merge(sleeper_adp_df, rankings_df, on='match col', suffixes=('_1','_2'), how='outer')
        df = df.drop(columns=['match col', 'Name_1'])
        df = df.rename(columns={'Name_2': 'Name'})

        df.to_csv(f'CheatSheet_{pos}.csv',index=False)