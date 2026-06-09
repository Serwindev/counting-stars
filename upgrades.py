import json

map = {
    0: "mouse",
    1: "intern"
}

with open("./details.json") as f:
    data = json.load(f)

def getMouse():
    return data[map[0]]

def upgrade(id, level):
    up = map[id-1]
    data[up][level] -= 0.05
    
    with open("./details.json", "w") as f:
        json.dump(data, f)