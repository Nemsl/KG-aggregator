Description of this knowledge graph aggregator

NECESSARY MODULES -------------
nltk
fastapi
rdflib
uvicorn (for fast api)
aiofiles

FAST API ---------------
You can start the aggregation from fast api by running Kombiner. You must specify what directory
of files you want to aggregate as an argument. We have two directories you can chose from: kg_filer_kort(35 files),
and kg_filer(354 files).


RUN FROM PYTHON -----------------
You can start the aggregation with the Kombinerer() function, located in the kombiner.py file.
Kombinerer() takes in one argument, the file path to where your knowledge graphs to be aggregated are stored.
It should be string and not include the final slash. Ex: Kombinerer('desktop/aFolder/graphs')
There are two folders already in the project folder, "kg_filer", and "kg_filer_kort"