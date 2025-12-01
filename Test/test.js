// Autor - Artus Klemm
var number = 0
var answers = []

function getWinnerPosition(list) {
  var index = 0
  for (let i = 0; i < list.length; i++){
    if (list[i] > list[index]) {            //võtab sisendiks listi punktidest mis iga positsioon sai ja tagastab
      index = i                             //positsiooni nime mille abil saab kuvada tuelmuste sõnastikust õige teksti
    }
  }
  const positions = ["side", "nurk", "diago", "tempo", "libero", "treener", "pink"] 
  return positions[index]
}

async function getData() {
  let response = await fetch("./küsimused.json")  //loeb sisse ja parse'ib küsimused.json sisu
  let data = await response.json()
  return data
}

async function nextQuest(x) {
  let data = await x
  let questions = data["questions"] 

  if (number < 6) {       //kui on veel küsimusi siis näitab pärast igat clicki uut küsimust
    document.getElementById("kysimus").textContent=(questions[number]["text"])
    document.getElementById("choice1").textContent=(questions[number]["answers"][0]["text"])
    document.getElementById("choice2").textContent=(questions[number]["answers"][1]["text"])
    document.getElementById("choice3").textContent=(questions[number]["answers"][2]["text"])
    document.getElementById("choice4").textContent=(questions[number]["answers"][3]["text"])
    updateProgress();     //uuendab progress bar'i
    number++
  }
  else {      //kui küsimused on otsas
    updateProgress()
    var pos = [0, 0, 0, 0, 0, 0, 0]
    for (let i = 0; i <= 5; i++) {
      const weights = data["questions"][i]["answers"][answers[i]]["scores"]  
      pos[0] += weights["side"]       //arvutab kõikide positsioonide punktisummad
      pos[1] += weights["nurk"]
      pos[2] += weights["diago"]
      pos[3] += weights["tempo"]
      pos[4] += weights["libero"]
      pos[5] += weights["treener"] 
      pos[6] += weights["pink"]
    }
    const position = getWinnerPosition(pos)  //vaatab milline positsioon sai kõige rohkem punkte
    document.getElementById("kysimus").textContent=("Oled: " + data["results"][position][0])  //kuvab tulemuse lehele
    document.getElementById("vastus").textContent=(data["results"][position][1])
    document.getElementById("choice1").style.display = "none"   //muudab nupud nähtamatuks
    document.getElementById("choice2").style.display = "none"
    document.getElementById("choice3").style.display = "none"
    document.getElementById("choice4").style.display = "none"
  }
}

function updateProgress() {   //uuendab progressbari näitama õiget progressi
  const bar = document.getElementById("progressBar");  
  const total = 6;   
  const percent = (number / total) * 100;
  bar.style.width = percent + "%";
}

async function choice(quest) {  //nupu vajutuse peale salvestab vastuse answers listi ning siis kuvab järmise küsimuse
  answers.push(quest)
  nextQuest(data)
}

const data = getData()  //et ei peaks iga kord faili uuesti lugema
nextQuest(data)     //teeb nii et lehe laadides näidataks õiget küsimust ja vastust



