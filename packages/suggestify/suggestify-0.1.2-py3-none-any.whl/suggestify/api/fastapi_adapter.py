from fastapi import FastAPI, Query
from suggestify import QuerySuggester

app = FastAPI()
suggester = QuerySuggester()

@app.get("/suggest")
def suggest(q: str = Query(...)):
    return suggester.suggest(q)
