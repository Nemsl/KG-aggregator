from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD
import os

#fetches the graph
def HentUt(index, dire):
    g = Graph()

    teller = 0
    nameList = []
    directory = os.fsencode(dire + '/')

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".ttl"):
            nameList.append(filename)
        else:
            continue
    #try and excepts so the function can accept many different formats
    try:
        return g.parse(location=dire + '/' + nameList[index], format="turtle")
    except:
        try:
            return index.parse(location=dire, format="turtle")
        except:
            return g.parse(location=dire + '/' + index +'.ttl', format="turtle")


#fetches exclusively from kombinerte_grafer
def HentKombinert(index):
    g = Graph()

    directory = os.fsencode('kombinerte_grafer/')

    return g.parse(location='kombinerte_grafer/' + os.fsdecode(os.listdir(directory)[index]), format="turtle")


#fetches text from graphs
def HentTekst(navn, dire, pt):
    # try and excepts so the function can accept many different formats
    if pt == True:
        try:
            g = HentUt(navn, dire)
        except:
            g = navn
    else:
        try:
            print('her')
            g = Graph()
            g.parse(location=dire + '/' + str(navn) + '.ttl', format="turtle")
        except:
            print('yeeh')

    qres2 = g.query("""
                    PREFIX nhterm: <https://newshunter.uib.no/term#>
                        SELECT ?text WHERE {
                            ?graph nhterm:originalText ?text .	
                        }""")
    textlist = []
    for row in qres2:
        text = str(row)
        try:
            textlist.append(text.split("rdflib.term.Literal('")[1].split("', datatype=rdflib.term.URIRef(")[0])
        except:
            textlist.append(text.split('rdflib.term.Literal("')[1].split('", datatype=rdflib.term.URIRef(')[0])

    return textlist

#fetches time from graphs
def HentTid(navn, dire):
    try:
        g = Graph()
        g.parse(location='GodeNavn/' + str(navn) + '.ttl', format="turtle")
    except:
        g = HentUt(navn, dire)

    qres2 = g.query("""
                    PREFIX nhterm: <https://newshunter.uib.no/term#>
                        SELECT ?text WHERE {
                            ?graph nhterm:sourceDateTime ?text .	
                        }""")
    klokkeliste = []
    for row in qres2:
        klokka = str(row)
        try:
            klokka = klokka.split("rdflib.term.Literal('")[1].split("', datatype=rdflib.term.URIRef(")[0]
        except:
            klokka = klokka.split('rdflib.term.Literal("')[1].split('", datatype=rdflib.term.URIRef(')[0]

        #formats the time object
        klokka = klokka.split('T')[0] + '\n' + klokka.split('T')[1].split('+')[0] + '\n' + \
                 klokka.split('+')[1]
        klokkeliste.append(klokka)

    return klokkeliste

#fetches from relevantenavn
def HentRelevanteNavn():
    path = "relevante_navn"
    liste = []
    for i in (os.listdir(path)):
        navn = i.split(".ttl")[0]
        liste.append(navn)
    return liste