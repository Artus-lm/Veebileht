// Autor - Artus Klemm
var number = 0
var answers = []

function getWinnerPosition(list) {
  var index = 0
  for (let i = 0; i < list.length; i++){
    if (list[i] > list[index]) {
      index = i
    }
  }
  const positions = ["side", "nurk", "diago", "tempo", "libero", "treener", "pink"] 
  return positions[index]
}

async function getData() {
  let response = await fetch("./küsimused.json")
  let data = await response.json()
  return data
}

async function initial(x){
  let data = await x
  document.getElementById("kysimus").textContent=(data["questions"][0]["text"])
  document.getElementById("choice1").textContent=(data["questions"][0]["answers"][0]["text"])
  document.getElementById("choice2").textContent=(data["questions"][0]["answers"][1]["text"])
  document.getElementById("choice3").textContent=(data["questions"][0]["answers"][2]["text"])
  document.getElementById("choice4").textContent=(data["questions"][0]["answers"][3]["text"])
} 

async function nextQuest(x) {
  let data = await x
  let questions = data["questions"]
  let results = data["results"]
  

  if (number < 6) {
    document.getElementById("kysimus").textContent=(data["questions"][number]["text"])
    document.getElementById("choice1").textContent=(data["questions"][number]["answers"][0]["text"])
    document.getElementById("choice2").textContent=(data["questions"][number]["answers"][1]["text"])
    document.getElementById("choice3").textContent=(data["questions"][number]["answers"][2]["text"])
    document.getElementById("choice4").textContent=(data["questions"][number]["answers"][3]["text"])
    number++
  }
  else {
    var pos = [0, 0, 0, 0, 0, 0, 0]
    for (let i = 0; i <= 5; i++) {
      const weights = data["questions"][i]["answers"][answers[i]]["scores"]
      pos[0] = pos[0] + weights["side"]
      pos[1] = pos[1] + weights["nurk"]
      pos[2] = pos[2] + weights["diago"]
      pos[3] = pos[3] + weights["tempo"]
      pos[4] = pos[4] + weights["libero"]
      pos[5] = pos[5] + weights["treener"] 
      pos[6] = pos[6] + weights["pink"]
    }
    const position = getWinnerPosition(pos)
    document.getElementById("kysimus").textContent=("Oled... " + data["results"][position][0])
    document.getElementById("vastus").textContent=(data["results"][position][1])
    document.getElementById("choice1").style.display = "none"
    document.getElementById("choice2").style.display = "none"
    document.getElementById("choice3").style.display = "none"
    document.getElementById("choice4").style.display = "none"
  }
}

const data = getData()

async function choice(quest) {
  answers.push(quest)
  nextQuest(data)
}

nextQuest(data)

