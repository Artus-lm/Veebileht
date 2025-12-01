// Autor - Artus Klemm
function textTo(element, field) {  //abifuntksioon mis loob field sisuga textNode'i ja lisab selle elemendile lapseks (aka teeb nii et elemnt kuvaks seda teksti)
    const text = document.createTextNode(field)
    element.appendChild(text)
}

async function createTable() {                               //loob mangud.json faili põhjal tabeli olnud ja tulevastest mängudest
    let response = await fetch("./autoupdate/mangud.json")
    let data = await response.json()                        //loeb json faili ja parse'ib selle
    const scoreboard = document.getElementById("tabel")     //hangib tabeli elemendi

    for (let i = 0; i < data.length; i++) {

        const row = document.createElement("tr") //loob ühe rea kõik vajalikud lahtrid
        var date = document.createElement("td")
        var time = document.createElement("td")
        var loc = document.createElement("td")
        var team1 = document.createElement("td")
        var team2 = document.createElement("td")
        var games = document.createElement("td")

        row.classList.add("row")        //lisab kõikidele lahtritele classid et neid saaks css'iga muuta
        date.classList.add("tdate")
        time.classList.add("ttime")
        loc.classList.add("tloc")
        team1.classList.add("t1")
        team2.classList.add("t2")
        games.classList.add("tgames")

        textTo(date, data[i]["date"])       //lisab kõikidesse lahtritesse mis kindlasti olemas on teksti
        textTo(time, data[i]["time"])
        textTo(loc, data[i]["location"])
        textTo(team1, data[i]["home"])
        textTo(team2, data[i]["away"])

        if (data[i]["state"] == "Done") {   //lisab lahtritesse ka puntkid kui mäng on toimunud
            textTo(games, data[i]["home_points"] + " - " + data[i]["away_points"])
        }
        else {textTo(games, "   -   ")}    //kui mäng pole toimunud lisab lahtrisse lihtsalt miinuse

        row.appendChild(date)       //lisab kõik lahtrid ritta
        row.appendChild(time)
        row.appendChild(loc)
        row.appendChild(team1)
        row.appendChild(games)
        row.appendChild(team2)

        scoreboard.appendChild(row) //lisab rea tabelisse
    }

}

createTable()       //laeb koos lehega ka tabeli
