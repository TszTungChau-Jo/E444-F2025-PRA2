from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
Bootstrap(app)   # initialize Flask-Bootstrap
Moment(app)      # initialize Flask-Moment


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def index():
    # Default: use my real name here
    name = "Joshua"
    return render_template("user.html", name=name, current_time=datetime.utcnow())

# keep the dynamic route too (optional, nice for testing)
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name, current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True)
