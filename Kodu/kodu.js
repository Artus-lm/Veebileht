// Autor - Artus Klemm
function textTo(element, field) {
    const text = document.createTextNode(field)
    element.appendChild(text)
}

async function createTable() {
    let response = await fetch("./autoupdate/mangud.json")
    let data = await response.json()
    for (let i = 0; i < data.length; i++) {

        const row = document.createElement("tr")
        var date = document.createElement("td")
        var time = document.createElement("td")
        var loc = document.createElement("td")
        var team1 = document.createElement("td")
        var team2 = document.createElement("td")
        var games = document.createElement("td")

        row.classList.add("row")
        date.classList.add("tdate")
        time.classList.add("ttime")
        loc.classList.add("tloc")
        team1.classList.add("t1")
        team2.classList.add("t2")
        games.classList.add("tgames")

        textTo(date, data[i]["date"])
        textTo(time, data[i]["time"])
        textTo(loc, data[i]["location"])
        textTo(team1, data[i]["home"])
        textTo(team2, data[i]["away"])

        if (data[i]["state"] == "Done") { 
            textTo(games, data[i]["home_points"] + " - " + data[i]["away_points"])
        }
        else {textTo(games, "   -   ")}
        row.appendChild(date)
        row.appendChild(time)
        row.appendChild(loc)
        row.appendChild(team1)
        row.appendChild(games)
        row.appendChild(team2)
        const scoreboard = document.getElementById("tabel")
        scoreboard.appendChild(row)
    }

}

createTable()
