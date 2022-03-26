import rdflib
import henter

def sammenliknNoder(g1, g2, dire):
    #fetches predicate and object to compare
    qres1 = g1.query("""
                    PREFIX nhterm: <https://newshunter.uib.no/term#>
                        SELECT ?p ?o WHERE {
                          ?s ?p ?o .
                        } LIMIT 100""")
    liste1 = []
    liste1Ord = []
    for row in qres1:
        for i in row:
            liste1.append(i)
    for i in liste1:
        #
        if 'http' not in str(i):
            liste1Ord.append(i)
        if 'resource' in str(i):
            liste1Ord.append(i)
    #fetches second graph for comparison
    qres2 = g2.query("""
                    PREFIX nhterm: <https://newshunter.uib.no/term#>
                        SELECT ?p ?o WHERE {
                          ?s ?p ?o .
                        } LIMIT 100""")
    liste2 = []
    liste2Ord = []
    for row in qres2:
        for i in row:
            liste2.append(i)
    poengsum = 0
    for i in liste2:
        if 'http' not in str(i):
            liste2Ord.append(i)
        if 'resource' in str(i):
            liste2Ord.append(i)

    #checks if nodes from the first graph appear in the second
    for i in liste1Ord:
        if i in liste2Ord:
            poengsum += 1
    k = henter.HentTekst(g2, dire, pt=True)

    #checks if objects from the first graph appear in the original text of the second
    allerede_sjekket = []
    for i in range(len(liste1)):
        if i % 2 == 0:
            for u in range(len(k)):
                if str(liste1[i]) == k[u]:
                    if liste1[i + 1] in allerede_sjekket:
                        continue
                    elif liste1[i + 1] == k[u + 1]:
                        poengsum += 1
                        allerede_sjekket.append(liste1[i + 1])

    #divides the sum of points by the length so longer graphs don't have an advantage
    poengsum = (poengsum / (len(liste1Ord) + len(liste2Ord) + 1)) * 10

    return poengsum