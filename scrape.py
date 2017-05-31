from bs4 import  BeautifulSoup
import requests

url1 = "https://www.espnfc.us/club/"
url2 = "/fixtures?leagueId=23"
clubs = ["afc-bournemouth/349", "arsenal/359", "burnley/379", "chelsea/363", "crystal-palace/384", "everton/368", "hull-city/306", "leicester-city/375", "liverpool/364", "manchester-city/382", "manchester-united/360", "middlesbrough/369", "southampton/376", "stoke-city/336", "sunderland/336", "swansea-city/318", "tottenham-hotspur/367", "watford/395", "west-bromwich-albion/383", "west-ham-united/371"]

#format urls
cluburls = ["" for i in range(0, len(clubs))]
for i in range(0, len(cluburls)):
    cluburls[i] = url1 + clubs[i] + url2

#find and write data from each page of fixtures
for i in range(0, len(cluburls)):
    page = requests.get(cluburls[i])
    if page.status_code < 400:
        club = clubs[i]
        clubname = club[:club.index('/')]
        soup = BeautifulSoup(page.content, "html.parser")
        matches = soup.findAll("div", id="club-fixtures")[0].findAll("div", "games-container")[1].findAll("a", href=True)
        csv = clubname + ".csv"
        f = open(csv, "w")
        for m in matches:
            match_link = m['href']
            match_link = match_link.replace("report","matchstats")
            match = requests.get(match_link)
            if match.status_code < 400:
                soup = BeautifulSoup(match.content, "html.parser")
                #get home/away teams
                teams = soup.find_all("div", "team-container")
                ht = teams[0].find_all("span", "long-name")[0].text
                at = teams[1].find_all("span", "long-name")[0].text
                #get goals scored
                goals = soup.find_all("div", "score-container")
                home = goals[0].span.text.strip()
                away = goals[1].span.text.strip()
                #get shots on target
                div = soup.find_all("div", "sub-module match-stats soccer")[0].find_all("div", "shots")
                shots = div[0].find_all("span", "number")
                hshots = shots[0].text
                ashots = shots[1].text
                data = ht + " v " + at + ", " + home + ", " + hshots + ", " + away + ", " + ashots + "\n"
                print(data)
                f.write(data)
        f.close()
