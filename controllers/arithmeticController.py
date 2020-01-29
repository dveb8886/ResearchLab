def add(a, b):
    return str(int(a)+int(b))

def calc_graph(dataset):
    redTotal = 0
    red = []
    blueTotal = 0
    blue = []
    cyanTotal = 0
    cyan = []

    for i in range (len(dataset[0])):
        redTotal += dataset[0][i]
        red.append(redTotal)
        blueTotal += dataset[1][i]
        blue.append(blueTotal)
        cyanTotal += (dataset[0][i] + dataset[1][i])
        cyan.append(cyanTotal)

    return [red, blue, cyan]