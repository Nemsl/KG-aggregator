import poeng_teller
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from fil_navn_generator import generator


def Kombiner(dire):

    print('kjørt fra kombiner')
    graphList = poeng_teller.PoengTeller(dire)
    teller = 0
    print(graphList)
    for u in graphList:
        teller += 1
        g = Graph()
        #bruke construct med vocabularies
        for i in u:
            g += i

        g.serialize(destination='kombinerte_grafer/' + str(teller) + ".ttl", format="turtle")
    generator()

