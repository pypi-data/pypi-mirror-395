import sys
import os

# Try different import strategies
def import_query_suggester():
    # Strategy 1: Try absolute import (installed package)
    try:
        from suggestify.core.suggester import QuerySuggester
        return QuerySuggester
    except ImportError:
        pass
    
    # Strategy 2: Try relative import (development)
    try:
        from .core.suggester import QuerySuggester
        return QuerySuggester
    except ImportError:
        pass
    
    # Strategy 3: Direct import (fallback)
    # Get the directory containing this __init__.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        from core.suggester import QuerySuggester
        return QuerySuggester
    except ImportError as e:
        raise ImportError(f"Cannot import QuerySuggester. Tried: suggestify.core.suggester, .core.suggester, core.suggester. Error: {e}")

QuerySuggester = import_query_suggester()

__all__ = ["QuerySuggester"]
__version__ = "0.1.2"