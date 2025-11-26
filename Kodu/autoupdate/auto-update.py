import bs4, requests

#
#  ---- Disclaimer ----
# File needs minor formating after program run.
# You need to remove last coma after the "}"
#

# --- Options ---

team = "Structura/Tartu vald "                  # team name + ' ' for specific team or None for all teams
save_to = "autoupdate/mangud.json"              # save file path
site_url = "https://evf-web.dataproject.com/CompetitionMatches.aspx?ID=84&PID=126"


# --- Functions ---

def find_length(list, date):
    count = 0
    for i, value in enumerate(list):
        if value == date:
            count += 1
            match count:
                case 3:
                    first = i
                case 4:
                    secnd = i - first
                    return i + secnd      
    return -1

def checkIfDate(item, date_of_reference, current_date_counter, current_counter):
    if item == date_of_reference:
        current_date_counter += 1
        if current_date_counter < 4:
            current_counter = -1
    return current_date_counter, current_counter

def dataExtract(unextracted_list):
    extracted = []
    while unextracted_list != []:
        temp = []
        counter = 0
        date_counter = 0
        name_compiler = ""
        venue_compiler = ""
        reference_date = unextracted_list[0]
        for i in unextracted_list:
            date_counter, counter = checkIfDate(i, reference_date, date_counter, counter)
            counter += 1
            match date_counter, counter:
                case 1, 0 | 2:
                    temp.append(i)
                case 1, 1:
                    pass
                case 1, _:
                    venue_compiler += i + " "
                case 2, 0:
                    temp.append(venue_compiler)
                case 3, 0 | 1 | 2:
                    pass
                case 3, _:
                    try:
                        temp.append(int(i))
                    except:
                        if i == '-':
                            temp.append(name_compiler)
                            name_compiler = ""
                        else:
                            name_compiler += i + " "
                case 4, _:
                    temp.append(name_compiler)
                    extracted.append(temp[:])
                    unextracted_list = unextracted_list[find_length(unextracted_list, reference_date):]
                    break
    return extracted
# could probably merge these two into one function and extract subfunctions out to make it more readable
def playoffsExtract(ploffs):
    extracted = []
    while ploffs != []:
        if ploffs[1] == "No":
            extracted.append([ploffs[0], "TBA"])
            ploffs = ploffs[5:]
        else:
            temp = [ploffs[0]]
            counter = -1
            date_counter = 0
            name_compiler = ""
            venue_compiler = ""
            reference_date = ploffs[1]
            for i in ploffs:
                if i == reference_date:
                    date_counter += 1
                    counter = -1
                counter += 1
                match date_counter, counter:
                    case 1, 0 | 2:
                        temp.append(i)
                    case 1, 1:
                        pass
                    case 1, _:
                        venue_compiler += i + " "
                    case 2, 0:
                        temp.append(venue_compiler)
                    case 3, 0 | 1 | 2:
                        pass
                    case 3, _:
                        try:
                            temp.append(int(i))
                        except:
                            if i == '-':
                                temp.append(name_compiler)
                                name_compiler = ""
                            else:
                                name_compiler += i + " "
                    case 4, length:
                        temp.append(name_compiler)
                        extracted.append(temp[:])
                        ploffs = ploffs[find_length(ploffs, reference_date)+1:]
                        break
    return extracted


# --- main body ---


response = requests.get(site_url, headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(response.text, features="html.parser")

site_text = soup.body.get_text(' ', strip=True)    # https://stackoverflow.com/questions/69593352/how-to-get-all-copyable-text-from-a-web-page-python

data = site_text[site_text.find("Matches Põhiturniir")+20:(site_text.find("Play-Off Play-Off") - len(site_text))]  # removes all text that isnt needed
playoffs = site_text[site_text.find("Play-Off Play-Off")+26:-77]

extracted = dataExtract(data.split())
extracted_playoffs = playoffsExtract(playoffs.split())


# --- Saving ---


json_file = open(save_to, mode="w", encoding="UTF-8")

json_file.write("[")
for i in extracted:
    if (team == None) | (team in i):
        if len(i) == 7:
            json_file.write(f"""
    {{
        "date": "{i[0]}",
        "time": "{i[1]}",
        "location": "{i[2]}",
        "home_points": "{i[3]}",
        "home": "{i[4]}",
        "away_points": "{i[5]}",
        "away": "{i[6]}",
        "state": "Done"
    }},
""")
        else:
            json_file.write(f"""
    {{
        "date": "{i[0]}",
        "time": "{i[1]}",
        "location": "{i[2]}",
        "home": "{i[3]}",
        "away": "{i[4]}",
        "state": "TB"
    }},
""")

for i in extracted_playoffs:
    if i[1] == "TBA":
        pass
    elif len(i) == 7:
        json_file.write(f"""
    {{
        "date": "{i[0]}",
        "time": "{i[1]}",
        "location": "{i[2]}",
        "home_points": "{i[3]}",
        "home": "{i[4]}",
        "away_points": "{i[5]}",
        "away": "{i[6]}",
        "state": "Done"
    }},
""")
    else:
        json_file.write(f"""
    {{
        "date": "{i[0]}",
        "time": "{i[1]}",
        "location": "{i[2]}",
        "home": "{i[3]}",
        "away": "{i[4]}",
        "state": "TB"
    }},
""")

json_file.write("]")

json_file.close()
