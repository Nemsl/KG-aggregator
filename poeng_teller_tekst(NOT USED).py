import Henter
import NodeSammenlikner
import Klokkesammenlikner
import os


def PoengTeller():
    directory = os.fsencode('KGfiler')
    sameEvent = {}

    for i in range(len(os.listdir(directory))):

        print('Base-Graph:', i)
        graph1 = Henter.hentUt(i)

        # gets text from first graph here so it does not do it every loop
        qres = graph1.query("""
            PREFIX nhterm: <https://newshunter.uib.no/term#>
                SELECT ?text WHERE {
                    ?graph nhterm:originalText ?text .	
                }""")
        texten1 = ''
        for row in qres:
            texten1 = str(row)

        thisGraphList = []  # blir lagt til som keys i sameEvent
        for y in range(len(os.listdir(directory))):
            if y == i:
                continue

            # sets variables to 0 and empty string so it doues not carry over from previous loop
            totalPoeng = 0
            texten2 = ''

            # gets text from second graph
            graph2 = Henter.hentUt(y)
            qres2 = graph2.query("""
                    PREFIX nhterm: <https://newshunter.uib.no/term#>
                        SELECT ?text WHERE {
                            ?graph nhterm:originalText ?text .	
                        }""")
            boolean = False
            for row in qres2:
                boolean = True
                texten2 = str(row)

            if not boolean:
                continue

            # textScore = Jaccard(texten1, texten2)

            # checks the score of
            nodeScore = NodeSammenlikner.sammenliknNoder(i, y)
            klokkeScore = Klokkesammenlikner.sammenliknKlokka(i, y)

            if nodeScore > 0.8:
                print(nodeScore, ' ---------------------------------------')
                if klokkeScore > 0.6:
                    thisGraphList.append(graph2)
        if len(thisGraphList) > 0:
            sameEvent[graph1] = thisGraphList

    returnlisten = []
    print(sameEvent)
    for iteringvar in sameEvent:
        # print(iteringvar.serialize(format="turtle").decode())

        returnlisten2 = []
        returnlisten2.append(iteringvar)

        for a in sameEvent[iteringvar]:
            # print(a.serialize(format="turtle").decode())
            returnlisten2.append(a)
            returnlisten.append(returnlisten2)

        # print(g.serialize(format="turtle").decode())
    return returnlisten
