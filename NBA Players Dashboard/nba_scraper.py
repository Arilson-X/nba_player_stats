from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.nba.com/teams'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

def trata_html(input):
    input = input.decode('ISO-8859-1')
    return " ".join(input.split()).replace('> <', '><')

def retorna_keys(soup):
    list_keys = []
    soup.findAll('th')
    for item in soup.findAll('th'):
        list_keys.append((item.get_text()))
    return list_keys

def get_name_teams():
    try:
        req = Request(url, headers = headers)
        response = urlopen(req)
        html = response.read()
        
    except HTTPError as e:
        print(e.status, e.reason)
        
    except URLError as e:
        print(e.reason)
    
    # html = html.decode('ISO-8859-1')
    html = trata_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    name_teams = soup.find_all("a", {"class": "TeamFigure_tfMainLink__OPLFu"})
    names = []
    for team in name_teams:
        str_teams = str(team)
        str_teams = str_teams.replace("%","")
        str_teams = str_teams.replace(".","")
        team = str_teams[str_teams.find('target="_blank"'):str_teams.find('</a>')]
        team = team.replace('target="_blank">','')
        names.append(team)

    return names

def get_figure_teams():
    try:
        req = Request(url, headers = headers)
        response = urlopen(req)
        html = response.read()
        
    except HTTPError as e:
        print(e.status, e.reason)
        
    except URLError as e:
        print(e.reason)
    
    # html = html.decode('ISO-8859-1')
    html = trata_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    figure_teams = soup.find_all("img", {"class": "TeamLogo_logo__PclAJ"})
    figures = []
    for team in figure_teams:
        str_teams = str(team)
        str_teams = str_teams.replace("%","")
        figure = str_teams[str_teams.find('src="'):str_teams.find('" title')]
        figure = figure.replace('src="','')
        figures.append(figure)

    return figures[:30]

figures_teams = get_figure_teams()
teams_names = get_name_teams()
id = [
    'BOS','BRK','NYK','PHI','TOR',
    'CHI','CLE','DET','IND','MIL',
    'ATL','CHO','MIA','ORL','WAS',
    'DEN','MIN','OKC','POR','UTA',
    'GSW','LAC','LAL','PHI','SAC',
    'DAL','HOU','MEM','NOP','SAS'
]

df = pd.DataFrame()
df['Tm'] = id
df['Names'] = teams_names
df['Images'] = figures_teams

df.to_csv("links_logo_nbs.csv",index=False)
