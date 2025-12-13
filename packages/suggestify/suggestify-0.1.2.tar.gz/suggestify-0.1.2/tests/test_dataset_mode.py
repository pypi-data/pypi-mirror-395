# tests/test_dataset_mode.py
import pytest
from suggestify.core.suggester import QuerySuggester

# --- Sample datasets ---
string_data = ["Alice", "Bob", "Charlie"]
dict_data = [
    {"name": "Python Tutorial"},
    {"name": "JavaScript Guide"},
    {"name": "Data Science Basics"}
]

def test_list_dataset():
    suggester = QuerySuggester(data_source=string_data)
    query = "Alice"
    suggestions = suggester.suggest(query, top_k=3)
    assert len(suggestions) > 0
    assert any("Alice" in s for s in suggestions)

def test_dict_dataset():
    suggester = QuerySuggester(data_source=dict_data, dict_field="name")
    query = "Python"
    suggestions = suggester.suggest(query, top_k=3)
    assert len(suggestions) > 0
    assert any("Python" in s for s in suggestions)

def test_multi_word_query():
    suggester = QuerySuggester(data_source=dict_data, dict_field="name")
    query = "Data Science Basics"
    suggestions = suggester.suggest(query, top_k=3)
    assert len(suggestions) > 0
    assert any("Data Science" in s for s in suggestions)

def test_ai_only_mode():
    suggester = QuerySuggester()
    query = "Diabetes"
    suggestions = suggester.suggest(query, top_k=5)
    assert len(suggestions) > 0
    assert any("Diabetes" in s for s in suggestions)

def test_empty_query():
    suggester = QuerySuggester()
    suggestions = suggester.suggest("", top_k=5)
    assert isinstance(suggestions, list)
