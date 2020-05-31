import snap
import os
import datetime
from datetime import timedelta, date
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from snap import TNEANet
from math import log10
from random import choice



os.chdir('./src')

def date_range(start_date, end_date):
    d = []
    for n in range(int ((end_date - start_date).days)):
        d.append(start_date + timedelta(n))
    return d

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    if continuous_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            if named_entity.strip() != '':
                continuous_chunk.append(named_entity)

    return continuous_chunk

def process_metadata(filename):
    st = ''

    with open(filename, "r") as file:
        for line in file:
            st += line
        st = st[st.find('\\') + 2:]
        st = st[st.find('\\') + 2:]
        st = st.strip()
        st = st[:-2]

    return st

def getCathegories(filename):
    return get_continuous_chunks(process_metadata(filename))[:-1]

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

def populate_with_metadata(network, dictionary):
    with open("Cit-HepTh-dates.csv", "r") as file:
        c = 0
        for line in file:
            if not c == 0: 
                l = line.split(',')
                nodeId = int(l[0])
                date = l[1]

                try:
                    file2 = './metadata/' + str(nodeId) + '.abs'
                    with open(file2, 'r'):
                        cathegories = getCathegories(file2)
                        
                except FileNotFoundError as err:
                    continue

                network.AddNode(nodeId)
                network.AddStrAttrDatN(nodeId, date, 'Date')

                for i, label in enumerate(cathegories):
                    if label.strip() != '':
                        network.AddStrAttrDatN(nodeId, label, 'label' + str(i))
                        if not label in dictionary:
                            dictionary[label] = 1
                        else:
                            dictionary[label] += 1
                
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

def populate_with_random_metadata(network, dictionary):
    with open("Cit-HepTh-dates.csv", "r") as file:
        c = 0
        for line in file:
            if not c == 0: 
                l = line.split(',')
                nodeId = int(l[0])
                date = l[1]

                try:
                    file2 = './random-metadata/' + str(nodeId) + '.abs'
                    with open(file2, 'r'):
                        cathegories = getCathegories(file2)
                        
                except FileNotFoundError as err:
                    continue

                network.AddNode(nodeId)
                network.AddStrAttrDatN(nodeId, date, 'Date')

                for i, label in enumerate(cathegories):
                    if label.strip() != '':
                        network.AddStrAttrDatN(nodeId, label, 'label' + str(i))
                        if not label in dictionary:
                            dictionary[label] = 1
                        else:
                            dictionary[label] += 1
                
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

def showIfHomophilyExists(type_of):
    network = TNEANet.New()

    ocurrence_dict = {}

    if type_of == 'normal':
        populate_with_metadata(network, ocurrence_dict)
    else:
        populate_with_random_metadata(network, ocurrence_dict)

    same_attribute = 0
    SNNE = 0 # número total de ocorrencias de tudo
    hypothetic_probability = 0
    for value in ocurrence_dict.values():
        SNNE += value

    for label, value in ocurrence_dict.items():
        hypothetic_probability += (value/SNNE) ** 2


    for e in network.Edges():
        n1, n2 = e.GetSrcNId(), e.GetDstNId()
        l1, l2 = [], []

        try:
            i = 0
            var = network.GetStrAttrDatN(n1, 'label' + str(i))
            while var.strip() != '':
                l1.append(var)
                i += 1
                var = network.GetStrAttrDatN(n1, 'label' + str(i)) 
        except:
            pass

        try:
            i = 0
            var = network.GetStrAttrDatN(n2, 'label' + str(i))
            while var.strip() != '':
                l2.append(var)
                i += 1
                var = network.GetStrAttrDatN(n2, 'label' + str(i)) 
        except:
            pass

        for element in l1:
            if element in l2:
                same_attribute += 1

    AD = same_attribute/SNNE # Actual distribution

    print("Hypothetic probability is:", hypothetic_probability)
    print("Actual distribution is:", AD)

def networkWithinDate(network, start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    minimum = datetime.datetime.strptime('2050-01-01', '%Y-%m-%d').date()
    maximum = datetime.datetime.strptime('1050-01-01', '%Y-%m-%d').date()
    node_set = set()

    ret_net = TNEANet.New()
    for node in network.Nodes():
        # print(node.GetId(), network.GetStrAttrDatN(node.GetId(), 'Date'))
        date = network.GetStrAttrDatN(node, 'Date').strip()
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        if date > maximum: maximum = date
        if date < minimum: minimum = date

        if date >= start and date <= end:
            nodeId = node.GetId()
            ret_net.AddNode(nodeId)
            ret_net.AddStrAttrDatN(nodeId, str(date), 'Date')
            node_set.add(nodeId)

    #print("minimum", minimum, "maximum", maximum)

    for edge in network.Edges():
       if edge.GetSrcNId() in node_set and edge.GetDstNId() in node_set:
           ret_net.AddEdge(edge.GetSrcNId(), edge.GetDstNId())

    return ret_net
           
def getMean(network):
    DegToCntV = snap.TIntPrV()
    snap.GetInDegCnt(network, DegToCntV)

    total_nodes = 0
    total_degree = 0
    for item in DegToCntV:
        total_nodes += item.GetVal2()
        total_degree += item.GetVal1()
    
    return total_degree/total_nodes

def getStandartDeviation(network, mean):
    DegToCntV = snap.TIntPrV()
    snap.GetInDegCnt(network, DegToCntV)

    total_nodes = 0
    total_deviation = 0
    for item in DegToCntV:
        total_nodes += item.GetVal2()
        total_deviation += abs(item.GetVal1() - mean)

    return total_deviation/total_nodes

def testPowerLaw(network, k, a, c):
    """
    k the number of citations
    a the constant 
    c the exponent
    """
    DegToCntV = snap.TIntPrV()
    snap.GetInDegCnt(network, DegToCntV)

    total_nodes = 0
    actual = 0
    for item in DegToCntV:
        total_nodes += item.GetVal2()
        if item.GetVal1() == k:
            actual = item.GetVal2()
    
    return str("%.3f" % log10(actual/total_nodes)) + ' = ' + str("%.3f" % (log10(a) - c*log10(k)))

def proveRichGetRicher(network):

    network = TNEANet.New()
    populate(network)


    start_date = date(1992, 3, 21)
    end_date = date(1999, 12, 31)
    dates = date_range(start_date, end_date)
    s = set()
    probability_sum = 0
    counter = 0

    for index, current_date in enumerate(dates[2:], start=1):
        if index == 1:
            last_network = networkWithinDate(network, dates[0].strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d")) 

            for element in last_network.Nodes():
                    if not element.GetId() in s:
                        s.add(element.GetId())

        else:
            curr_d = current_date.strftime("%Y-%m-%d")
            new_network = networkWithinDate(network, dates[0].strftime("%Y-%m-%d"), curr_d)
            new_papers_id = []

            for node in new_network.Nodes():
                if not node.GetId() in s:
                    new_papers_id.append(node.GetId())

            for new_paper_id in new_papers_id:
                random_id = choice(tuple(s))
                for edge in new_network.Edges():
                    if edge.GetSrcNId() == new_paper_id:
                        probability_sum += 1/(len(s))
                        for e in new_network.Edges():
                            if e.GetSrcNId() == random_id:
                                if edge.GetSrcNId() == e.GetDstNId():
                                    counter += 1


            for element in new_network.Nodes():
                    if not element.GetId() in s:
                        s.add(element.GetId())
            last_network = new_network

    print("Probability sum", probability_sum, "Counter", counter)


showIfHomophilyExists('normal')
showIfHomophilyExists('weird')
#showIfHomophilyExists('normal')

#ret_net = networkWithinDate(network,'1999-12-01','1999-12-2')

# for n in ret_net.Nodes():
#     print(n.GetId(), ret_net.GetStrAttrDatN(n.GetId(), 'Date'))

# network = TNEANet.New()
# oc_dict = {}
# populate_with_metadata(network, oc_dict)
# print(getAverageEmbeddednessOfEdges(network))

# snap.PrintInfo(network, "Python type PNEANet")
