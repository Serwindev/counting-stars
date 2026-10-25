import json

map = {
    0: "mouse",
    1: "intern"
}

with open("./details.json") as f:
    data = json.load(f)

def default():
    if data["overall"]["isNew"] == True:
        data["mouse"] = {
        "time": 0.5,
        "count": 1,
        "level": 1,
        "cost": 10,
        "active": True
    }
        data["intern"] = {
        "time": 1,
        "count": 2,
        "level": 1,
        "cost": 50,
        "active": False
    }
        data["overall"] = {
        "isNew": False,
        "total_count": 0,
        "count": 0
    }

    with open("./details.json", "w") as f:
            json.dump(data, f)

def init():
    sum = 0
    for key in data:
        val = data[key].keys()
        if "active" in val:
            if data[key]["active"] == True:
                sum += data[key]["count"]

    data["overall"]["total_count"] = sum

    with open("./details.json", "w") as f:
        json.dump(data, f)

def getMouse():
    return data[map[0]]

def getIntern():
    return data[map[1]]

def upgradeMouse(level):
    if level == "time":
        if data["mouse"]["time"] > 0.1:
            up = map[0]
            data[up][level] -= 0.05
            data[up]["cost"] += 20
            data[up]["level"] += 1
    
    with open("./details.json", "w") as f:
        json.dump(data, f)

def upgradeIntern(level):
    if level == "time":
        if data["intern"]["time"] >= 0.6:
            up = map[1]
            data[up][level] -= 0.01
            data[up]["cost"] += 25
            data[up]["level"] += 1
            data[up]["active"] = True

    with open("./details.json", "w") as f:
            json.dump(data, f)

def saveData(count, total_count):
    data["overall"]["count"] = count
    data["overall"]["total_count"] = total_count

    with open("./details.json", "w") as f:
        json.dump(data, f)

def getCount(id = 0):
    if id == 1:
        return data["overall"]["total_count"]
    return data["overall"]["count"]