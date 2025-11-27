import bs4, requests, json

# --- Options ---

wanted_team = "Structura/Tartu vald"            # team name for specific team or None for all teams
save_to = "./Kodu/autoupdate/mangud.json"        # save file path
site_url = "https://evf-web.dataproject.com/CompetitionMatches.aspx?ID=84&PID=126"


# --- Functions ---

def findLength(list, date):
    count = 0
    for i, value in enumerate(list):
        if (value == date) & (i != 0):
            return i
    print("Error, could not find second date in findLength")


def getLoc(list, reference_date):
    location = ""

    for i in range(10):
        location += list[0]
        list = list[1:]

        if list[0] == reference_date:
            return list, location
        location += " "

    print("Error, did not find 2nd reference date in getLoc")
    

def getTeam1(list):
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
    team = ""
    for i in range(10):
        team += list[0]
        list = list[1:]
        if list[0] == reference_date:
            return list, team
        team += " "
    print("Error, did not encounter reference date in getTeam2")


def areAnnounced(list):
    if list[0] != "Finaal":
        return False, True, True, True, True
    
    finaal = False
    thirdfourth = False
    pool = False
    veerand = False

    if list[16] == "No":                                #if first statement is true all matches must be false,
        return True, finaal, thirdfourth, pool, veerand #if the second is true the first couldnt be so first match must be true
    if list[11] == "No":                                # and all others false and so on
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
            unextracted_list[1:]
        
        reference_date = unextracted_list[0]

        temp = {"date" : reference_date, "time" : unextracted_list[2]}
        unextracted_list = unextracted_list[3:]
        

        unextracted_list, temp["location"] = getLoc(unextracted_list, reference_date)
        unextracted_list = unextracted_list[3:]

        names_length = findLength(unextracted_list, reference_date)
        unextracted_list, temp["home"] = getTeam1(unextracted_list)

        if unextracted_list[0] == "-":
            temp["state"] = "TB"
            unextracted_list = unextracted_list[1:]
        else: 
            temp["home_points"] = unextracted_list[0]
            temp["away_points"] = unextracted_list[2]
            temp["state"] = "Done"
            unextracted_list = unextracted_list[3:]
        
        unextracted_list, temp["away"] = getTeam2(unextracted_list, reference_date)
        unextracted_list = unextracted_list[names_length:]
        if (temp["home"] == wanted_team) | (temp["away"] == wanted_team) | (wanted_team == None):
            extracted.append(temp)

    pass
    return extracted


# --- main body ---


response = requests.get(site_url, headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(response.text, features="html.parser")

site_text = soup.body.get_text(' ', strip=True)    # https://stackoverflow.com/questions/69593352/how-to-get-all-copyable-location-from-a-web-page-python

data = site_text[site_text.find("Matches Põhiturniir")+20:(site_text.find("Play-Off Play-Off") - len(site_text))]  # removes all text that isnt needed
playoffs = site_text[site_text.find("Play-Off Play-Off")+26:-77]

extracted = dataExtract(data.split())
extracted_playoffs = dataExtract(playoffs.split())


# --- Saving ---

to_write = extracted + extracted_playoffs

with open(save_to, mode="w", encoding="UTF-8") as jfile:
    json.dump(to_write, jfile, indent=4, ensure_ascii=False)