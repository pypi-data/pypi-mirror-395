from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggestify import QuerySuggester

suggester = QuerySuggester(data_source=None)  # DB optional

@api_view(["GET"])
def suggest(request):
    query = request.GET.get("q", "")
    return Response(suggester.suggest(query))
