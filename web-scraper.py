import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import pymongo

def format_teams(string):
    pattern = '\(.+\)'

    if "/" in string: 
        string = string.replace(" / ",",")

    n = re.sub(pattern, '', string)
    return list(n.split(","))

    

def count_accolades(string):
    if type(string) == float:
        return 'none'
    else:
        string_list = string[1:-1]
        chips_list = list(string_list.split(","))
        count = len(chips_list)
        return count


URL = "https://en.wikipedia.org/wiki/NBA_75th_Anniversary_Team"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")

results = soup.find('table',{'class':"wikitable sortable plainrowheaders"})

df = pd.read_html(str(results))

df = pd.DataFrame(df[0])

# drop the unwanted columns
data = df.drop(["Ref."], axis=1)

data.rename(columns={'Name[5]': 'name', 
		     'Team(s) played for (years)[note 3]': 'teams',
		     'Pos': 'position',
		     'Pts': 'points',
		     'Reb': 'rebounds',
		     'Ast': 'assists',
		     'Championships won[b]': 'championships',
		     'MVP won': 'regular_seasons_mvps',
		     'Finals MVP won': 'finals_mvps',
		     'All Star': 'all_star',
		     'All-NBA': 'all_nba', 
		     'HoF Year': 'hof_year'}, inplace=True)


data_dict = data.to_dict("records")


# iterate over the dataframe row by row
for index_label, row_series in data.iterrows():
    # For each row update the 'Bonus' value to it's double
    x = data.at[index_label, 'teams']
    y = format_teams(x)
    data.at[index_label , 'teams'] = y

    c = data.at[index_label, 'championships']   
    chips = count_accolades(c)
    data.at[index_label , 'championships'] = chips

    rmvp = data.at[index_label, 'regular_seasons_mvps']   
    m = count_accolades(rmvp)
    data.at[index_label , 'regular_seasons_mvps'] = m

    fmvp = data.at[index_label, 'finals_mvps']   
    f = count_accolades(fmvp)
    data.at[index_label , 'finals_mvps'] = f
   
teams = 'Cincinnati Royals / Kansas City-Omaha / Kansas City Kings (1970-1976) New York Nets (1976-1977) Boston Celtics (1978-1983) Milwaukee Bucks (1983-1984)'
print(data)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["75-best-nba-players"]
players = mydb["players"]

data.reset_index(inplace=True)
data_dict = data.to_dict("records")

players.delete_many({})
for row in data.to_dict(orient="records"):
        players.insert_one(row)

