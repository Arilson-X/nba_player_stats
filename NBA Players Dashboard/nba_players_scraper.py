from selenium import webdriver
from  selenium.webdriver.common.keys import Keys
from  selenium.webdriver.common.by import By
from  selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

url = 'https://www.nba.com/players'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
x_path = '//*[@id="__next"]/div[2]/div[2]/main/div[2]/section/div/div[2]/div[1]/div[7]/div/div[3]/div/label/div/select'

def get_players():
    driver.get("https://www.nba.com/players")
    sleep(5)
    select_element = driver.find_element(By.XPATH,x_path)
    select = Select(select_element)
    select.select_by_visible_text('All')
    table_element = driver.find_element(By.XPATH,'//table')
    table_html = table_element.get_attribute('outerHTML')
    driver.quit()
    df = pd.read_html(table_html,extract_links='body')
    return(df[0])

def formata_nome(nome):
    posicoes = []
    for indice, caractere in enumerate(nome):
        if caractere.isupper():
            posicoes.append(indice)
    sobrenome = nome[posicoes[1]:]
    nome = nome[:posicoes[1]]

    return nome + ' ' + sobrenome

def retorna_image_link(link):
    string = "https://cdn.nba.com/headshots/nba/latest/260x190/"
    number = link.split("/")[2]

    return string+number+'.png'

def formata_coluna(coluna):
    list = []
    for valor in df[coluna]:
        list.append(valor[0])
    return list

df = get_players()
list_players_name = []
list_players_image_link = []
for player in df['Player']:
    list_players_name.append(formata_nome(player[0]))
    list_players_image_link.append(retorna_image_link(player[1]))

df['Name'] = list_players_name
df['Image'] = list_players_image_link
df.drop('Player', axis=1, inplace=True)

for column in df.columns:
    if column != "Name" and column != "Image":
        df[column] = formata_coluna(column)

print(df.head())

df.to_csv("player_complement_nbs.csv",index=False)
