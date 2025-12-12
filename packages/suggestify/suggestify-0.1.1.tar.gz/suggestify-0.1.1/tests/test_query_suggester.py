from suggestify.core.suggester import QuerySuggester

# Sample mock dataset
mock_data = ["Alice", "Bob", "Charlie"]


def test_suggester_with_data():
    # Initialize with mock data
    suggester = QuerySuggester(data_source=mock_data)
    
    query = "Alice"
    suggestions = suggester.suggest(query, top_k=3)
    
    # Check it returns something relevant
    assert len(suggestions) > 0
    assert any("Alice" in s for s in suggestions)

def test_suggester_without_data():
    # AI-only mode (no dataset)
    suggester = QuerySuggester()
    
    query = "Diabetes"
    suggestions = suggester.suggest(query, top_k=5)
    
    # Should return AI-generated suggestions
    assert len(suggestions) == 5
    # Example: one suggestion contains the query
    assert any(query in s for s in suggestions)
