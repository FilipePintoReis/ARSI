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

def showClusteringCoefficient(network):
    DegToCCfV = snap.TFltPrV()
    result = snap.GetClustCfAll(network, DegToCCfV)
    for item in DegToCCfV:
        print("degree: %d, clustering coefficient: %f" % (item.GetVal1(), item.GetVal2()))
    print("average clustering coefficient", result[0])
    print("closed triads", result[1])
    print("open triads", result[2])


def getEdgeBridges(network):
    UGraph = snap.ConvertGraph(snap.PUNGraph, network)

    EdgeV = snap.TIntPrV()
    snap.GetEdgeBridges(UGraph, EdgeV)

    for edge in EdgeV:
        print("edge: (%d, %d)" % (edge.GetVal1(), edge.GetVal2()))
    print(len(EdgeV))
    return EdgeV

def getAverageEmbeddednessOfEdges(network):
    m = {}
    for edge in network.Edges():
        if edge.GetSrcNId() in m:
            m[edge.GetSrcNId()].append(edge.GetDstNId())
        else:
            m[edge.GetSrcNId()] = [edge.GetDstNId()]
     
    counter = 0
    for edge in network.Edges():
        for n1 in m[edge.GetSrcNId()]:
            if edge.GetDstNId() in m and n1 in m[edge.GetDstNId()]:
                counter += 1

    return counter/network.GetEdges()

def getAnEdgeEmbeddedness(network, edge):
    m = {}
    for e in network.Edges():
        if e.GetSrcNId() in m:
            m[e.GetSrcNId()].append(e.GetDstNId())
        else:
            m[e.GetSrcNId()] = [e.GetDstNId()]
    
    counter = 0
    for n1 in m[edge.GetSrcNId()]:
        if edge.GetDstNId() in m and n1 in m[edge.GetDstNId()]:
            counter += 1

    return counter


network = TNEANet.New()

populate(network)


print(getAverageEmbeddednessOfEdges(network))

#snap.PrintInfo(network, "Python type PNEANet")


