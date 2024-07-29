from requests_html import HTMLSession
import pandas as pd

def pull_sleeper_ADP(position='all', format='ppr', league='dynasty'):
    # Assumes a 12-man league size

    base_url = 'https://www.draftsharks.com/adp/'
    format_url = '' if format == 'standard' else format + '/'
    league_url = '' if league == 'redraft' else league + '/'
    position_url = '' if position == 'all' else position + '/'

    full_url = base_url + league_url + format_url + 'sleeper/12/' + position_url

    session = HTMLSession()
    response = session.get(full_url)
    response.html.render()  # This renders the JavaScript content
    
    # Find the span with class 'name'
    name_data = response.html.find('span.name')
    pos_data = response.html.find('span.position')
    team_data = response.html.find('span.team')
    names = [name.full_text for name in name_data]
    adps = list(range(1, len(names) + 1))
    positions = [pos.full_text for pos in pos_data]
    teams = [team.full_text for team in team_data]
    
    # Create a DataFrame
    df = pd.DataFrame({ 'SleeperADP': adps, 'Name': names, 'Position': positions, 'Team': teams})

    return df
    
if __name__ == "__main__":
    #test the code
    sleeper_data = pull_sleeper_ADP()
    print(sleeper_data)