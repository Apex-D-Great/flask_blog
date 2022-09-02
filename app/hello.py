from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> hello kwam</h1>"

# custom error pages 

# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html"), 404

# internal server error
@app.errorhandler(500)
def server_error(e):
    return render_template("error500.html"), 500