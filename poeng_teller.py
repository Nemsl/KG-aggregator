import henter
import node_sammenlikner
import klokke_sammenlikner
import os

#gives
def PoengTeller(dire):
    directory = os.fsencode(dire)
    sameEvent = {}

    #loops through and compares all the graphs
    for i in range(len(os.listdir(directory))):
        print('Base-Graph:', i)
        klokke1 = henter.HentTid(i, dire)
        # gets added as keys in sameEvent
        thisGraphList = []

        #loops through graphs that should be compared with graph1
        g1 = henter.HentUt(i, dire)

        for y in range(len(os.listdir(directory))):

            #if graph1 and graph2 are the same graph do nothing
            if y == i:
                continue
            g2 = henter.HentUt(y, dire)
            klokke2 = henter.HentTid(y, dire)

            #sets variables to 0 and empty string so it doues not carry over from previous loop
            totalPoeng = 0
            texten2 = ''


            #checks similarity of nodes and time
            nodeScore = node_sammenlikner.sammenliknNoder(g1, g2, dire)
            klokkeScore = klokke_sammenlikner.SammenliknKlokka(klokke1, klokke2)
            #if the graphs are sufficiently similar and close in timeframe they will be combined
            if nodeScore > 0.8 and klokkeScore > 0.6:
                thisGraphList.append(henter.HentUt(y, dire))

        #if one other similar graph was found it will be turned into a dictionary
        if len(thisGraphList) > 0:
            sameEvent[g1] = thisGraphList


    #generates and returns the list of lists with graphs that should be combined
    returnlisten = []
    print(sameEvent)
    for iteringvar in sameEvent:
        returnlisten2 = []
        returnlisten2.append(iteringvar)
        for a in sameEvent[iteringvar]:
            returnlisten2.append(a)
            returnlisten.append(returnlisten2)

    return returnlisten
