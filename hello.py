from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
Bootstrap(app)   # initialize Flask-Bootstrap
Moment(app)      # initialize Flask-Moment

@app.route("/")
def index():
    # use your real name here
    name = "Joshua"
    return render_template("user.html", name=name, current_time=datetime.utcnow())

# keep the dynamic route too (optional, nice for testing)
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name, current_time=datetime.utcnow())

if __name__ == "__main__":
    app.run(debug=True)
