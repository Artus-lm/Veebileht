import bs4, requests, json

#
#   This is a file to parse all the data we need from 
#   the evf-web.dataproject.com site to a .json file.
#   This way we dont need to look up any data byhand,
#   only run this once in a while to update all the information.
#

# --- Options ---

# team name for specific team or None for all teams
wanted_team = "Structura/Tartu vald"  
# save file path
save_to = "./Kodu/autoupdate/mangud.json"   
# website url to get data from
site_url = "https://evf-web.dataproject.com/CompetitionMatches.aspx?ID=84&PID=126"


# --- Helper Functions ---

def findLength(list, date):      
    # gets the length of data that we need to remove at the end 
    count = 0
    for i, value in enumerate(list):
        if (value == date) & (i != 0):
            return i
    print("Error, could not find second date in findLength")


def getLoc(list, reference_date):       
    # Gets the location
    location = ""

    for _ in range(10):
        location += list[0]
        list = list[1:]

        if list[0] == reference_date:
            return list, location
        location += " "

    print("Error, did not find 2nd reference date in getLoc")
    

def getTeam1(list):         
    # Gets the first teams name
    team = ""
    list = list[3:]
    for i in range(10):
        team += list[0]
        list = list[1:]
        if list[0] == "-":
            return list, team
        try: 
            int(list[0])
            return list, team      
        except:
            team += " "
    print('Error, did not encounter number or "-" in getTeam1')
        

def getTeam2(list, reference_date):     
    # Gets the second teams name
    team = ""
    for i in range(10):
        team += list[0]
        list = list[1:]
        if list[0] == reference_date:
            return list, team
        team += " "
    print("Error, did not encounter reference date in getTeam2")


def areAnnounced(list):         
    # Checks if the list is of the play-offs or not and 
    # after that checks which games have been announced
    if list[0] != "Finaal":
        return False, True, True, True, True
    
    finaal = False
    thirdfourth = False
    pool = False
    veerand = False

    # if first statement is true all matches must be false,
    # if the second is true the first couldnt be so first match must be true
    # and all others false and so on
    if list[16] == "No":                                
        return True, finaal, thirdfourth, pool, veerand 
    if list[11] == "No":                                
        veerand = True
        return True, finaal, thirdfourth, pool, veerand
    if list[6] == "No":
        pool = True
        return True, finaal, thirdfourth, pool, veerand
    if list[1] == "No":
        thirdfourth = True
        return True, finaal, thirdfourth, pool, veerand
    print("Error, could not identify if the games are announced in areAnnounced")

# --- Main Function ---

def dataExtract(unextracted_list):
    extracted = []
    plofs, finaal, thirdfourth, pool, veerand = areAnnounced(unextracted_list)  

    if plofs:                   
        # Checks if the list is of the play-offs or not and 
        # cuts out all the games that havent been announced
        if not veerand:
            unextracted_list = [] 
        elif not pool:
            unextracted_list = unextracted_list[15:] 
        elif not thirdfourth:
            unextracted_list = unextracted_list[10:] 
        elif not finaal:
            unextracted_list = unextracted_list[5:] 


    while unextracted_list != []:
        
        if plofs:               
            # if they are the playoffs then each section starts with the name of the match
            unextracted_list[1:]
        
        # gets the date of the match, this is used to keep track how to parse the upcoming data
        reference_date = unextracted_list[0]      

        # gets the date and the time then removes them from the list
        temp = {"date" : reference_date, "time" : unextracted_list[2]}      
        unextracted_list = unextracted_list[3:]
        
        # gets the location and then removes the next date and time from the list
        unextracted_list, temp["location"] = getLoc(unextracted_list, reference_date)       
        unextracted_list = unextracted_list[3:]

        # finds how much data we need to remove at the end to get to
        # the next match and then gets the home team
        names_length = findLength(unextracted_list, reference_date)         
        unextracted_list, temp["home"] = getTeam1(unextracted_list)

        # Checks if the match has been held and if it has gets the points and
        # after that removes them from the list
        if unextracted_list[0] == "-":          
            temp["state"] = "TB"
            unextracted_list = unextracted_list[1:]
        else: 
            temp["home_points"] = unextracted_list[0]
            temp["away_points"] = unextracted_list[2]
            temp["state"] = "Done"
            unextracted_list = unextracted_list[3:]
        
        # Gets the away team and then removes the unneeded data from the list
        unextracted_list, temp["away"] = getTeam2(unextracted_list, reference_date)
        unextracted_list = unextracted_list[names_length:]

        # checks if the team we want takes part in the match, if not then throws out the data
        if (temp["home"] == wanted_team) | (temp["away"] == wanted_team) | (wanted_team == None):   
            extracted.append(temp)

    return extracted


def main():
    # uses bs4 to get all the text from the site
    # i got this idea from https://stackoverflow.com/questions/69593352/how-to-get-all-copyable-location-from-a-web-page-python
    response = requests.get(site_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(response.text, features="html.parser")         

    site_text = soup.body.get_text(' ', strip=True)

    # formats the data a bit to make it suitable for parsing
    data_start = site_text.find("Matches Põhiturniir ") + len("Matches Põhiturniir ")       
    data_end = site_text.find("Play-Off Play-Off") - len(site_text)
    footer_length = 77
    plofs_start = site_text.find("Play-Off Play-Off") + len("Play-Off Play-Off Matches ")

    data = site_text[data_start:data_end]
    playoffs = site_text[plofs_start:-footer_length]

    # converts the data into a long list then parses it
    extracted = dataExtract(data.split())               
    extracted_playoffs = dataExtract(playoffs.split())

    # gathers all the data from both the games and the play-offs
    to_write = extracted + extracted_playoffs       

    # writes it all as json to a json file specified in the options part of the code
    with open(save_to, mode="w", encoding="UTF-8") as jfile:            
        json.dump(to_write, jfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
# this all could probably have been done by regex too, but i found out about it way too late. Also the data is in quite a difficult form

# for anyone wondering what the data looks like unparsed(linebreaks added for clarity):

# dd/mm/yyyy - hh:mm location name
# dd/mm/yyyy - hh:mm
# dd/mm/yyyy - hh:mm team 1 points1 - points2 team 2 
# dd/mm/yyyy - hh:mm points1 - points2 team 1 team 2

# and this is just one game