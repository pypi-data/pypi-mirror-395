# 🚀 Suggestify — AI Query Suggestion Engine

Suggestify intelligently generates search query recommendations using NLP.
Works **with or without a database** — fully plug & play. It can be used for any domain—technology, food, healthcare, geography, science, entertainment, and more.

---

## 🔥 Features

| Feature | Supported |
|---|---|
| Semantic AI suggestions | ✔ |
| Works without DB | ✔ |
| Fuzzy matching | ✔ |
| Django + FastAPI + Flask adapters | ✔ |
| SQL / CSV history intake | ✔ |

---

AI-Only Mode: Generate realistic query suggestions without any dataset.

Dataset Mode: Works with CSV, SQLite, or Python lists for enriched semantic + fuzzy search.

Semantic + Fuzzy Matching:
Powered by sentence-transformers and rapidfuzz.

Dynamic Query Generation:
Produces natural queries instead of simple completions.

Domain-Agnostic:
Works with any topic or dataset.

Entity Extraction (spaCy):
For even richer, contextual suggestions.

## 🚀 Installation

```bash  

pip install suggestify

python -m spacy download en_core_web_sm
```

## 🔗 Backend Integration

### FastAPI

```python
from fastapi import FastAPI
from suggestify import QuerySuggester

app = FastAPI()
suggester = QuerySuggester()
# or
suggester = QuerySuggester(data_source=your data_source)

@app.get("/suggest/")
def suggest(query: str):
    return {"suggestions": suggester.suggest(query, top_k=5)} # top_k - the number of suggestions you want to return.
```

#### Django REST Framework

views.py

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggestify import QuerySuggester

suggester = QuerySuggester()
# or
suggester = QuerySuggester(data_source=your data_source)

@api_view(['GET'])
def suggest_query(request):
    query = request.GET.get('query', '')
    return Response({"suggestions": suggester.suggest(query, top_k=5)}) # top_k - the number of suggestions you want to return.
```

urls.py

``` python
from django.urls import path
from .views import suggest_query

urlpatterns = [
    path("suggest/", suggest_query),
]
```

### ⚛ Frontend Example (React)

```javascript
import { useState } from "react";

export default function SuggestionApp() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  async function fetchSuggestions() {
    const res = await fetch(`/suggest/?query=${query}`);
    const data = await res.json();
    setSuggestions(data.suggestions);
  }

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your query..."
      />
      <button onClick={fetchSuggestions}>Get Suggestions</button>
      <ul>
        {suggestions.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
  );
}
```

📊 How It Works

AI-only mode:
Generates suggestions using NLP patterns, entity extraction, and dynamic templates.

Dataset mode:

Encodes dataset entries using sentence-transformers

Performs semantic search

Adds fuzzy matching for typos

Blends results into natural-language queries

Dynamic query generation:
Uses entity extraction + flexible template generation to craft realistic, domain-appropriate suggestions.

## License

[MIT](https://choosealicense.com/licenses/mit/)
