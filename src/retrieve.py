import bs4
import lxml
import pandas as pd
import urllib
import numpy
from bs4 import BeautifulSoup

# Retrieve the html page of a given link by using a firefox user agent to circumvent the connection refused error
def firefoxPage(link):
    req = urllib.request.Request(
        url=link, 
        headers={'User-Agent': 'Mozilla/5.0'} # IMPORTANT (sinon connection refusee)
    )
    html_page = urllib.request.urlopen(req)
    return html_page

# Getting the link of all the players of a given year and split of the region
def getPlayerLinkList(split_link_list):
    player_link_list = []
    for (link, year, split) in split_link_list:
        html_page = firefoxPage(link)
        soup = BeautifulSoup(html_page, features="lxml")
        for link in soup.find_all('a'):
            if str(link.get('href')).startswith("./player-stats/"):
                player_link_list.append((str(link.get('href')).strip('.'), year, split))
    return player_link_list


# Check if the "columns" or simply the html element of a table column is not empty
def checkCols(cols):
    if cols == None:
        return False
    for k in cols:
        if k != '':
            return True
    return False

# Get the stats of all players of the given list of players
def getPlayerStats(player_link_list):
    data = []
    columnNames = ['Player', 'Year', 'Split']
    generateCol = True
    for link, year, split in player_link_list:
        link = link.strip()
        html = firefoxPage("https://gol.gg/players" + link)
        soup = BeautifulSoup(html, features="lxml")

        table = soup.find("table", attrs={"class": "table_list"})
        name = soup.find("h1").text.strip()
        playerStat = [name, year, split]

        rows = table.find_all('tr')
        if columnNames != ['Player', 'Year', 'Split']:
            generateCol = False
        for row in rows:

            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            if checkCols(cols):
                if generateCol:
                    columnNames.append(cols[0])
                playerStat = playerStat + [elem for elem in cols[1:] if elem != '']
        data.append(playerStat)
    return pd.DataFrame(data, columns=columnNames)
    
# Get the links of all teams of the given list of splits
def getLCKTeamLinkList(split_link_list):
    team_link_list = []

    for (link, year, split) in split_link_list:
        html_page = firefoxPage(link)
        soup = BeautifulSoup(html_page, features="lxml")
        for link2 in soup.find_all('a'):
            if str(link2.get('href')).startswith("./team-stats/"):
                old, new = LCK_link_suffix(split, year)
                team_link_list.append((str(link2.get('href')).strip('.').replace(old, new), year, split))
    return team_link_list

def getLPLTeamLinkList(split_link_list):
    team_link_list = []

    for (link, year, split) in split_link_list:
        html_page = firefoxPage(link)
        soup = BeautifulSoup(html_page, features="lxml")
        for link2 in soup.find_all('a'):
            if str(link2.get('href')).startswith("./team-stats/"):
                old, new = LPL_link_suffix(split, year)
                team_link_list.append((str(link2.get('href')).strip('.').replace(old, new), year, split))
    return team_link_list

def getLECTeamLinkList(split_link_list):
    team_link_list = []

    for (link, year, split) in split_link_list:
        html_page = firefoxPage(link)
        soup = BeautifulSoup(html_page, features="lxml")
        for link2 in soup.find_all('a'):
            if str(link2.get('href')).startswith("./team-stats/"):
                old, new = LEC_link_suffix(split, year)
                team_link_list.append((str(link2.get('href')).strip('.').replace(old, new), year, split))
    return team_link_list

def getLCSTeamLinkList(split_link_list):
    team_link_list = []

    for (link, year, split) in split_link_list:
        html_page = firefoxPage(link)
        soup = BeautifulSoup(html_page, features="lxml")
        for link2 in soup.find_all('a'):
            if str(link2.get('href')).startswith("./team-stats/"):
                old, new = LCS_link_suffix(split, year)
                team_link_list.append((str(link2.get('href')).strip('.').replace(old, new), year, split))
    return team_link_list

# Returns the table element of the player's stats (team name is asked to find the right table in the page)
def get_player_table(soup, team_name):
    tables = soup.find_all('table')
    for table in tables:
        caption = table.find('caption')
        if caption and caption.text.strip() == team_name + ' player\'s stats':
            return table
        else:
            continue
    return None

# Returns a dataframe with the role of each player and the team and split they played in
def getPlayerRole(team_link_list):
    labels = ['Team', 'Year', 'Split','Role','Player']
    data = []

    for link, year, split in team_link_list:
        link = link.strip()
        html = firefoxPage("https://gol.gg/teams" + link)
        soup = BeautifulSoup(html, features="lxml")

        table = soup.find("table", attrs={"class": "table_list"})
        name = soup.find("h1").text.strip()
        rows = get_player_table(soup, name).find_all('tr')
        
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 2:
                stat = [name] # Team
                stat.append(year) # Year
                stat.append(split) # Split
                stat.append(tds[0].text.strip())  # Role
                stat.append(tds[1].text.strip()) # Player
                data.append(stat)
    return pd.DataFrame(data, columns=labels)

def getTeamStats(split_link_list):
    data = []
    labels = None
    for (link, year, split) in split_link_list:
        html_page = firefoxPage(link)
        soup = BeautifulSoup(html_page, features="lxml")
        table = soup.find_all('table')[1]
        rows = table.find_all('tr')
        if labels == None:
            labels = ['Year', 'Split'] + [elem.text.strip() for elem in table.find('thead').find_all('th')]
        for row in rows:
            stat = [year, split]
            tds = row.find_all('td')
            for td in tds:
                stat.append(td.text.strip())
            if (stat != [year, split]):
                data.append(stat)
    print(data)
    return pd.DataFrame(data, columns=labels)


# Auxillary function to get the suffix of the link of a given split and year of the LCK (Korean League)
def LCK_link_suffix(split, year):
    return ('LCK ' + split + ' ' + str(year) + '/','LCK%20' + split + '%20' + str(year) + '/')

# Auxillary function to get the suffix of the link of a given split and year of the LPL (Chinese League)
def LPL_link_suffix(split, year):
    return ('LPL ' + split + ' ' + str(year) + '/','LPL%20' + split + '%20' + str(year) + '/')

# Auxillary function to get the suffix of the link of a given split and year of the LEC (European League)
def LEC_link_suffix(split, year):
    return ('LEC ' + split + ' ' + str(year) + '/','LEC%20' + split + '%20' + str(year) + '/')

# Auxillary function to get the suffix of the link of a given split and year of the LCS (North American League)
def LCS_link_suffix(split, year):
    return ('LCS ' + split + ' ' + str(year) + '/','LCS%20' + split + '%20' + str(year) + '/')