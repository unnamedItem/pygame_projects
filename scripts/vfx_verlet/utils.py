import math, json

def read_json(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return json.loads(data)

def write_json(path, data):
    f = open(path, 'w')
    json.dump(data, f)
    f.close()

def get_dis(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
