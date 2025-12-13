from rapidfuzz import process

def fuzzy_match(query, corpus, limit=5):
    """Return spelling-close or substring suggestion fallback"""
    results = process.extract(query, corpus, limit=limit)
    return [match for match, score, _ in results if score > 60]
