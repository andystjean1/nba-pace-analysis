

from bs4 import BeautifulSoup
import requests
from nba_api.stats.static import teams

#gets a teams pace from basketball-reference.com
#parmeter: team_abv - the teams abbreviation - the team to get the pace for
# parameter: season - the season to get the pace for
def get_team_pace(team_abv, season):

    url ="https://www.basketball-reference.com/teams/{}/{}.html"

    url = url.format(team_abv, season)

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    strongs = soup.find_all('strong')
    strong_text = ""
    for s in strongs:
        if(s.text.lower() == "pace"):
            pace_strong = s
            strong_text = pace_strong.parent

    pace_text = strong_text.text.split(")")[1].strip()
    return pace_text.split(" ")[1] #should probably convert this to an itn here - or maybe just do it in the dataframe

# build the pace_dictionary
# parameter: season - the season for the pace statistics
# returns a dictionary with the team pace statistic for the given season
# dictionary: key = team_id : value = team's pace
def build_pace_dictionary(season):
    team_list = teams.get_teams()
    team_pace = {}

    for team in team_list:
        try:
            abv = team["abbreviation"]
            #print(abv)

            #make sure the abbreviation will match basketball-reference
            if(abv == "BKN"):
                pace = get_team_pace("BRK", season) #Nets
            elif(abv == "PHX"):
                pace = get_team_pace("PHO", season) #Suns
            elif(abv == "CHA"):
                pace == get_team_pace("CHO", season) #Hornets
            else:
                pace = get_team_pace(abv, season)

            team_pace[team["id"]] = pace
        except:
            print("This abbreviation doesnt fit in the URL ", team["abbreviation"])

    return team_pace

if __name__ == "__main__":
    print(build_pace_dictionary('2019'))
