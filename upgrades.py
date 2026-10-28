import json
import os

map = {
    0: "mouse",
    1: "intern"
}

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "details.json")

MOUSE_MIN_TIME = 0.1
MOUSE_STEP = 0.05
INTERN_MIN_TIME = 0.3
INTERN_STEP = 0.1
MAX_POWER = 10


def fresh():
    return {
        "mouse": {
            "time": 0.5,
            "count": 1,
            "level": 1,
            "cost": 10,
            "active": True,
            "powerLevel": 1,
            "powerCost": 25
        },
        "intern": {
            "time": 1,
            "count": 2,
            "level": 1,
            "cost": 50,
            "active": False,
            "powerLevel": 1,
            "powerCost": 80
        },
        "overall": {
            "isNew": False,
            "total_count": 0,
            "count": 0,
            "earned": 0,
            "caught": 0
        }
    }


def load():
    start = fresh()
    try:
        with open(SAVE_FILE) as f:
            saved = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return start


    for key in start:
        if key in saved:
            start[key].update(saved[key])
    return start


data = load()


def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def default():
    if data["overall"]["isNew"] == True:
        data.clear()
        data.update(fresh())
    save()


def init():
    data["mouse"]["time"] = round(data["mouse"]["time"], 2)
    data["intern"]["time"] = round(data["intern"]["time"], 2)

    if data["overall"]["count"] < 0:
        data["overall"]["count"] = 0

    data["overall"]["total_count"] = getTotalCount()
    save()


def getTotalCount():
    total = 0
    for key in data:
        if data[key].get("active") == True:
            total += data[key]["count"]
    return total


def getMouse():
    return data[map[0]]


def getIntern():
    return data[map[1]]


def upgradeMouse(level):
    mouse = data[map[0]]

    if level == "time":
        if mouse["time"] <= MOUSE_MIN_TIME:
            return False
        mouse["time"] = round(max(MOUSE_MIN_TIME, mouse["time"] - MOUSE_STEP), 2)
        mouse["cost"] += 20
        mouse["level"] += 1
        return True

    if level == "count":
        if mouse["powerLevel"] >= MAX_POWER:
            return False
        mouse["count"] += 1
        mouse["powerCost"] = int(mouse["powerCost"] * 1.6)
        mouse["powerLevel"] += 1
        return True

    return False


def upgradeIntern(level):
    intern = data[map[1]]

    if level == "time":
        if intern["active"] == False:

            intern["active"] = True
        elif intern["time"] <= INTERN_MIN_TIME:
            return False
        else:
            intern["time"] = round(max(INTERN_MIN_TIME, intern["time"] - INTERN_STEP), 2)
        intern["cost"] += 25
        intern["level"] += 1
        return True

    if level == "count":
        if intern["active"] == False or intern["powerLevel"] >= MAX_POWER:
            return False
        intern["count"] += 2
        intern["powerCost"] = int(intern["powerCost"] * 1.5)
        intern["powerLevel"] += 1
        return True

    return False


def saveData(count, total_count, earned=None):
    data["overall"]["count"] = count
    data["overall"]["total_count"] = total_count
    if earned is not None:
        data["overall"]["earned"] = earned
    save()


def getCount(id = 0):
    if id == 1:
        return data["overall"]["total_count"]
    return data["overall"]["count"]


def getEarned():
    return data["overall"]["earned"]