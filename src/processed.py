f1 = open("Cit-HepTh-dates.csv", "w")
f2 = open("Cit-HepTh.csv", "w")

d = {}

class Paper:
    def __init__(self, id, date):
        self.id = id
        self.date = date
        self.citations = set()

    def citates(self, citation):
        self.citations.add(citation)

with open("Cit-HepTh-dates.txt", "r") as file:
    c = 0
    f1.write("Id,Timestamp\n")
    for line in file:
        if not c == 0: 
            l = line.split()
            if l[0][0] == '1' and l [0][1] == '1':
                d[l[0][2:]] = Paper(l[0][2:], l[1])
                nl = l[0][2:] + "," + l[1] + '\n'
                f1.write(nl)
        else: 
            c += 1

with open("Cit-HepTh.txt", "r") as file:
    f2.write("Source,Target\n")
    for line in file:
        if c > 4:
            l = line.split()
            if l[0] in d and l[1] in d:
                nl = l[0] + "," + l[1] + '\n'
                f2.write(nl)
                d[l[0]].citates(l[1])
        else: 
            c += 1