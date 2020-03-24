f1 = open("unprocessed/Cit-HepTh-dates.csv", "w")
f2 = open("unprocessed/Cit-HepTh.csv", "w")

with open("unprocessed/Cit-HepTh-dates.txt", "r") as file:
    c = 0
    for line in file:
        if not c == 0: 
            l = line.split()
            nl = l[0] + "," + l[1] + '\n'
            f1.write(nl)
        else: 
            c += 1

with open("unprocessed/Cit-HepTh.txt", "r") as file:
    for line in file:
        if c > 4:
            l = line.split()
            nl = l[0] + "," + l[1] + '\n'
            f2.write(nl)
        else: 
            c += 1


class Paper:
    def __init__(self, id, date, citates):
        self.id = id
        self.date = date

