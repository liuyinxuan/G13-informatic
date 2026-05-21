from flask import Flask, render_template, request, flash
import search

app = Flask(__name__)
app.secret_key = "send_Help123"

"""
    install flask through pip first
    this is where you run the web GUI
    can simply run through main or through terminal by "flask run"
    follow the link to web GUI
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=['POST'])
def search_query():
    query = request.form['query_input']
    results = search.web_search(query)
    # summaries = [result['summary'] for result in results]
    flash(f"Search Result: {results}")
    if results is not None:
        return render_template("index.html", results = results)
    else:
        return "Search stopped"

if __name__ == "__main__":
    app.run(debug=True)