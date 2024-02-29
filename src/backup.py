def ambiguousPlayerName(soup):
    # mw-parser-output
    div = soup.find("div", {"class": "mw-parser-output"})
    link = soup.find("a")["href"]
    print(link)
    return firefoxRequest('https://lol.fandom.com/wiki' + link).find("table", {"class": "infobox infobox-player-narrow InfoboxPlayer"})
    
def getRole(name):
    name = normalizeName(name)
    html_page = firefoxRequest('https://lol.fandom.com/wiki/' + name)
    soup = BeautifulSoup(html_page, features="lxml")
    table = soup.find("table", {"class": "infobox infobox-player-narrow InfoboxPlayer"})
    if table is None:
        table = ambiguousPlayerName(soup)
    rows = table.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 2:
            if "Role" in tds[0].get_text(strip=True):
                return tds[1].get_text(strip=True)