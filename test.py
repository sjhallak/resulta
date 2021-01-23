import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

#-----------
import json
import requests
from datetime import datetime

st.title('Sam Hallak - Resulta challenge app')

# Defind date range here 
start_date = '2020-01-12'
end_date = '2020-01-19'

# API endpoints
scoreboard_url = "https://delivery.chalk247.com/scoreboard/NFL/{0}/{1}.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0".format(start_date, end_date)
team_rankings_url = "https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0"


# function definitions
def formatdate (date_time_str):
    dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    return dt.strftime('%d-%m-%Y')

def formattime (date_time_str):
    dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    return dt.strftime('%H:%M')

def roundup (str):
    x = float(str)
    return round(x,2)

def getteam(team_id):
    for item in teams:
        if item["team_id"] == team_id:
            return item



# --- program starts here ----

# --- Get team ranking data
response = requests.get(team_rankings_url)
json_data = json.loads(response.text)
teams = json_data['results']['data']
#print(json.dumps(teams, indent=4, sort_keys=True))
#team_df = pd.DataFrame(teams)
#print (team_df.sort_values('team'))


#--- Get scoreboard data
response = requests.get(scoreboard_url)
json_data = json.loads(response.text)
scoreboard = json_data['results']
#print(json.dumps(scoreboard, indent=4, sort_keys=True))

f = []
for x in scoreboard:
    eventDate = scoreboard[x]
    if 'data' in eventDate:
        events = eventDate['data']
        for e in events:
            f.append (events[e])

# event_df = pd.DataFrame(f).drop(['scoring'], 1)
# print(event_df.loc[:, ['event_id','event_date', 'event_date','away_team_id','away_nick_name','away_city', 'home_team_id','home_nick_name','home_city' ]])

# --- combine data into results 
results = []
for e in f:
   away_team = getteam(e['away_team_id'])
   home_team = getteam(e['home_team_id'])
   event_dict = {
      'event_id': e['event_id'],
      'event_date': formatdate(e['event_date']),
      'event_time': formattime(e['event_date']),
      'away_team_id': e['away_team_id'],
      'away_nick_name': e['away_nick_name'],
      'away_city': e['away_city'],
      'away_rank': away_team['rank'],
      'away_rank_points': roundup(away_team['adjusted_points']),
      'home_team_id': e['home_team_id'],
      'home_nick_name': e['home_nick_name'],
      'home_city': e['home_city'],
      'home_rank': home_team['rank'],
      'home_rank_points': roundup(home_team['adjusted_points']),
   }
   results.append(event_dict)

results_df = pd.DataFrame(results)
# print (results_df.sort_values('event_id'))

# voilà - results have the required events list.
#print('// Events for date range {0} to {1}'.format(start_date, end_date))
#print (results)

"""
### My first app using Streamlit 
#### Here's our first attempt at using data to create a table:
"""
msg = 'Showing Events for date range {0} to {1}'.format(start_date, end_date)
st.write(msg)


results_df
