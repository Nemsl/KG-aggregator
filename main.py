from fastapi import FastAPI
from fastapi.responses import FileResponse
import henter
import kombinerer
import os

#Assigns FastAPI() as a variable
app = FastAPI()




@app.get("/")
def VisKombinerteGrafer():
    return henter.HentRelevanteNavn()


#Kombines all graphs
@app.get("/Kombiner")
def Kommbiner(directory):
    kombinerer.Kombiner(str(directory))
    return {}

#Shows a selected file
@app.get("/{fil}")
def VisFil(fil):
    path = "relevante_navn"
    return FileResponse(path +'/' + str(fil)+'.ttl')

#Shows the texts in a file
@app.get("/{fil}/tekst")
def Tekst(fil):
    return henter.HentTekst(fil, 'relevante_navn', pt=False)

#Shows the dates in a file
@app.get("/{fil}/dato")
def Dato(fil):
    return henter.HentTid(fil, 'relevante_navn')
