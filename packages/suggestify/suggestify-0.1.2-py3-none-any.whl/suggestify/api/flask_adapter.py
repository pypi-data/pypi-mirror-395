from flask import Flask, request, jsonify
from suggestify import QuerySuggester

app = Flask(__name__)
suggester = QuerySuggester()

@app.route("/suggest")
def suggest():
    q = request.args.get("q", "")
    return jsonify(suggester.suggest(q))
