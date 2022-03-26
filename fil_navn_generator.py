import henter
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from sentence_transformers import SentenceTransformer
from collections import Counter
from shutil import copyfile
import klokke_sammenlikner

#generates a filename for each file in "kombinerte_grafer"
def generator():
    #loops through all combined files
    for i in range(len(os.listdir("kombinerte_grafer"))):
        graph1 = henter.HentKombinert(i)

        #selects only the text
        qres = graph1.query("""
                    PREFIX nhterm: <https://newshunter.uib.no/term#>
                        SELECT ?text WHERE {
                            ?graph nhterm:originalText ?text .	
                        }""")
        texten1 = ''

        #list with all originalTexts
        textListe = []

        for row in qres:
            texten1 = str(row)
            textListe.append(texten1)


        #adds only the first sentence
        mid = textListe
        textListe = []
        for b in mid:
            for u in b.split(". "):

                textListe.append(u)

        #reformats the text
        streng = ' '.join(map(str, textListe))
        try:
            streng = streng.replace("(rdflib.term.Literal('", "").replace("datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#string')),)", "").replace("https","")#.replace("datatype=rdflib.term.URIRef", "").replace("/", "").replace("www.w3.org/2001/XMLSchema", "")
        except:
            streng = streng.replace('(rdflib.term.Literal("', "").replace("datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#string')),)", "").replace("https","")#.replace("datatype=rdflib.term.URIRef", "").replace("/", "").replace("www.w3.org/2001/XMLSchema", "")

        #prepares the text for evaluation
        ord = streng.lower()
        ord = word_tokenize(ord)
        stop_words = set(stopwords.words('english'))

        #list of words that can bacome the filename
        ordStop = []

        #checks for bad or illegal filename elements
        for w in ord:
            if w not in stop_words and not w in ["''",'rdflib.term.literal', '``', ',', '.', '-', '"', "'", '?', '!', '(', ')', '”', '’', '“', '#', ':', 'http', '@', '‘', '/'] and not '\\' in w and not '|' in w and not "'" in w:
                ordStop.append(w)


        ord = ordStop


        def get_wordnet_pos(word):
            #lematizes each word
            tag = nltk.pos_tag([word])[0][1][0].upper()
            tag_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)

        #lematizes
        lemmatizer = WordNetLemmatizer()
        ord = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in ord]


        #counts the two most common words and finds out if they are similar to other files
        counts = Counter(ord)
        top_two = counts.most_common(2)
        teller = 0

        #list with files that shares the same name
        filerMedSammeNavn = []
        newName = ''
        for ii in top_two:
            if teller == 1:
                newName = newName + '_' + ii[0]
                topOrd = ii[0]
            else:
                newName = newName + ii[0]
                topOrd = ii[0]
            teller += 1

            #checks if the filenames are similar
            for qq in henter.HentRelevanteNavn():
                if topOrd in qq.split('_'):
                    filerMedSammeNavn.append(qq)



        #deletes duplicates
        filerMedSammeNavn=set(filerMedSammeNavn)
        filerMedSammeNavn=list(filerMedSammeNavn)


        #counts all datetime triples as there is only one for each graph
        qres3 = graph1.query("""
                                PREFIX nhterm: <https://newshunter.uib.no/term#>

                                SELECT (COUNT(*) AS ?count)
                                    WHERE
                                    {
                                      ?s nhterm:sourceDateTime ?o
                                    }""")

        #formats the count
        for row in qres3:
            lengdeOr = str(row).replace("(rdflib.term.Literal('", "").replace(
                "', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#integer')),)", "")

        #counts the amount of graphs in the second graph
        lengdeListe = []
        for graphs in filerMedSammeNavn :
            graph = henter.HentUt(graphs, 'relevante_navn')
            qres2 = graph.query("""
                        PREFIX nhterm: <https://newshunter.uib.no/term#>

                        SELECT (COUNT(*) AS ?count)
                            WHERE
                            {
                              ?s nhterm:sourceDateTime ?o
                            }""")
            for row in qres2:
                lengdeListe.append(row)

        #slett dictates if the first graph should be deleted
        slett = False

        #list of files that should be deleted
        filerSomSkalSlettes = []

        #compare the files based on size of the files and clock score
        teller2 = 0
        for ww in lengdeListe:
            ww = str(ww).replace("(rdflib.term.Literal('", "").replace("', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#integer')),)", "")
            tidDenne = henter.HentTid(i, "kombinerte_grafer")

            tidDenne = [tidDenne[0]]
            tidSammenliknMed = henter.HentTid(filerMedSammeNavn[teller2] , 'relevante_navn' )
            tidSammenliknMed = [tidSammenliknMed[0]]
            score = klokke_sammenlikner.SammenliknKlokka(tidDenne, tidSammenliknMed)


            #if this file is smaller than the compared file, and they are from a similar time period, it will not be added
            if int(lengdeOr) < int(ww) and score > 0.7:
                slett = True
            # if this file is bigger than the compared file, and they are from a similar time period, the compared file will be deleted
            elif int(lengdeOr) > int(ww) and score >=0.7:
                filerSomSkalSlettes.append(filerMedSammeNavn[teller2])


            teller2+=1


        newName = newName + '.ttl'
        filename = os.fsdecode(os.listdir("kombinerte_grafer")[i])

        for zz in filerSomSkalSlettes:
            zz = zz + '.ttl'
            os.remove('relevante_navn/' + zz)


        if slett == False:
            try:
                os.remove('relevante_navn/' + newName)
                copyfile('kombinerte_grafer/' + filename, 'relevante_navn/' + newName)
            except:
                copyfile('kombinerte_grafer/' + filename, 'relevante_navn/' + newName)

generator()