# suggestify/core/suggester.py
from sentence_transformers import SentenceTransformer, util
from suggestify.core.database import load_queries
from suggestify.core.fuzzy import fuzzy_match
import wikipediaapi
import spacy

# Load spaCy English model once
nlp = spacy.load("en_core_web_sm")

class QuerySuggester:
    def __init__(
        self,
        data_source=None,
        table=None,
        model_name='all-MiniLM-L6-v2',
        use_wiki=None,
        wiki_lang='en',
        user_agent="suggestify-bot",
        dict_field=None
    ):
        """
        Initialize the Query Suggestion Engine.
        - data_source: list, CSV path, or DB connection string
        - dict_field: if data_source is a list of dicts, pick this key as query text
        - use_wiki: None = auto (True if no dataset)
        """
        self.model = SentenceTransformer(model_name)
        self.data_source = data_source
        self.table = table
        self.dict_field = dict_field

        # Load dataset queries
        self.queries = load_queries(data_source, table)

        # If list of dicts, extract specified field
        if self.queries and isinstance(self.queries[0], dict):
            if not dict_field:
                raise ValueError("data_source is list of dicts, specify dict_field")
            self.queries = [d[dict_field] for d in self.queries if dict_field in d]

        self.embeddings = None
        if self.queries:
            self.embeddings = self.model.encode(self.queries, convert_to_tensor=True)

        # Wiki mode
        if use_wiki is None:
            self.use_wiki = not bool(self.queries)
        else:
            self.use_wiki = use_wiki

        if self.use_wiki:
            self.wiki = wikipediaapi.Wikipedia(language=wiki_lang, user_agent=user_agent)

    def _wiki_sentences(self, query, max_sentences=20):
        """Fetch first few sentences from Wikipedia page for the query"""
        if not self.use_wiki or not query.strip():
            return []
        page = self.wiki.page(query)
        if not page.exists():
            return []
        doc = nlp(page.text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        return sentences[:max_sentences]

    def _generate_dynamic_queries(self, query, sentences):
        """Generate query-style suggestions from sentences dynamically"""
        suggestions = []

        for sentence in sentences:
            doc = nlp(sentence)
            for chunk in doc.noun_chunks:
                noun = chunk.text.strip()
                if not noun:
                    continue

                # Skip nouns unrelated to main query
                if query.lower() not in noun.lower() and query.lower() not in sentence.lower():
                    continue

                # Common patterns
                if any(tok.dep_ in ["attr", "ROOT"] for tok in doc):
                    suggestions.append(f"What is {noun}?")

                verbs = [tok.lemma_ for tok in doc if tok.pos_ == "VERB"]
                if any(v in ["produce", "grow", "use", "make", "process", "manufacture"] for v in verbs):
                    suggestions.append(f"How is {noun} used?")
                    suggestions.append(f"Where is {noun} produced?")

                if any(tok.ent_type_ == "DATE" for tok in doc):
                    suggestions.append(f"History of {noun}")

                # Fallback
                suggestions.append(f"Learn about {noun}")

        # Deduplicate while preserving order
        return list(dict.fromkeys(suggestions))

    def suggest(self, query, top_k=5, use_fuzzy=True):
        """
        Generate top_k suggestions for a query:
        - Semantic search over dataset (if exists)
        - Wikipedia dynamic suggestions (if wiki mode enabled)
        - Optional fuzzy expansion
        """
        suggestions = []

        # --- Dataset Semantic Search ---
        if self.queries and self.embeddings is not None and query.strip():
            # Support multi-word queries by splitting into 3-word n-grams
            query_phrases = [query]
            words = query.split()
            if len(words) > 3:
                query_phrases = [" ".join(words[i:i+3]) for i in range(len(words)-2)]

            for qp in query_phrases:
                query_emb = self.model.encode(qp, convert_to_tensor=True)
                hits = util.semantic_search(query_emb, self.embeddings, top_k=top_k)[0]
                suggestions.extend([self.queries[h['corpus_id']] for h in hits])

        # --- Fuzzy Expansion ---
        if use_fuzzy and self.queries and query.strip():
            try:
                fz = fuzzy_match(query, self.queries)
                suggestions.extend([s for s in fz if s not in suggestions])
            except Exception:
                pass  # skip errors for unusual corpus items

        # --- Wikipedia Dynamic Queries ---
        if self.use_wiki and query.strip():
            sentences = self._wiki_sentences(query)
            wiki_suggestions = self._generate_dynamic_queries(query, sentences)
            suggestions.extend(wiki_suggestions)

        # Deduplicate and limit top_k
        final = []
        for s in suggestions:
            if s not in final:
                final.append(s)
            if len(final) >= top_k:
                break

        return final