import DateTime
import math

def SammenliknKlokka(klokke1, klokke2):
    #try and except to handle errors where some graph files may be empty
    try:
        #formats the time
        klokke1 = klokke1[0].split('\n')
        klokke1Liste = []
        klokke1Liste.append(klokke1[0].split('-'))
        klokke1Liste.append(klokke1[1].split(':'))
        klokke1 = klokke1Liste

        #turns the formatted time into a datetime object
        a = DateTime.DateTime(int(klokke1[0][0]), int(klokke1[0][1]), int(klokke1[0][2]), int(klokke1[1][0]),
                              int(klokke1[1][1]), int(klokke1[1][2]))
        if klokke2 != []:
            # formats the time

            klokke2 = klokke2[0].split('\n')
            klokke2Liste = []
            klokke2Liste.append(klokke2[0].split('-'))
            klokke2Liste.append(klokke2[1].split(':'))
            klokke2 = klokke2Liste

            # turns the formatted time into a datetime object
            b = DateTime.DateTime(int(klokke2[0][0]), int(klokke2[0][1]), int(klokke2[0][2]), int(klokke2[1][0]),
                                  int(klokke2[1][1]), int(klokke2[1][2]))

            c = a - b
            c = abs(c) * 100

            #runs an activation function on the result so it   lies between 1 and 0. 1 means the two times are identical
            cActive = (1 / (1 + math.exp(c))) * 2

            return cActive
        else:
            return 0
    except:
        return 0