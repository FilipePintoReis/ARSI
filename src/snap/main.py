import snap
from snap import TNEANet

import os

os.chdir('./src')


def populate(network):
    with open("Cit-HepTh-dates.csv", "r") as file:
        c = 0
        for line in file:
            if not c == 0: 
                l = line.split(',')
                nodeId = int(l[0])
                date = l[1]
                network.AddNode(nodeId)
                network.AddStrAttrDatN(nodeId, date, 'Date')
            else: 
                c += 1

    with open("Cit-HepTh.csv", "r") as file:
        c = 0
        for line in file:
            if not c == 0:
                l = line.split(',')
                srcNode = int(l[0])
                dstNode = int(l[1])
                network.AddEdge(srcNode, dstNode)
            else: 
                c += 1


network = TNEANet.New()

populate(network)

snap.PlotClustCf(network, "example", "Directed graph - clustering coefficient")