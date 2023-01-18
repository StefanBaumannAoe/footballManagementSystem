import requests
from bs4 import BeautifulSoup

url = "https://www.bfv.de/mannschaften/tv-altoetting/016PMD3330000000VV0AG80NVUT1FLRU"
with requests.get(url) as page:
    soup = BeautifulSoup(page.content, "html.parser")

    team_name = "TV Altötting"

    games = soup.find_all("tr", class_="game")
    for game in games:
        home_team = game.find("td", class_="home").find("span", class_="team-name").get_text()
        away_team = game.find("td", class_="away").find("span", class_="team-name").get_text()
        date = game.find("td", class_="date").get_text()
        if home_team == team_name or away_team == team_name:
            opponent = home_team if away_team == team_name else away_team
            print(f"{team_name} vs {opponent} on {date}")