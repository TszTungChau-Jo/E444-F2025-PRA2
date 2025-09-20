from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Flask-WTF / WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-change-me'  # required by Flask-WTF (CSRF/session)
Bootstrap(app)   # initialize Flask-Bootstrap
Moment(app)      # initialize Flask-Moment


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# ----- Flask-WTF form -----
class InfoForm(FlaskForm):
    username = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField(
    'What is your UofT Email address?',
    validators=[DataRequired(), Email()],
    render_kw={
        "required": True,
        "pattern": r"^[^@]+@[^@]*utoronto[^@]*$",
        "title": "Please use your UofT email (must contain '@mail.utoronto.ca')."
    }
)
    submit = SubmitField('Submit')


# ----- Routes -----
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        # detect changes and flash messages
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name and old_name != form.username.data:
            flash('Looks like you have changed your name!')
        if old_email and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        # store values in session and redirect (Post/Redirect/Get)
        session['name'] = form.username.data.strip()
        session['email'] = form.email.data.strip()
        return redirect(url_for('index'))

    # GET (or failed POST): compute ok flag from session
    name = session.get('name')
    email = session.get('email')
    ok = (email is not None and 'utoronto' in email.lower())

    return render_template('index.html',
                           form=form,
                           name=name,
                           email=email,
                           ok=ok,
                           current_time=datetime.utcnow())

# Route to refresh the page
@app.route('/reset')
def reset():
    session.clear()  # or: session.pop('name', None); session.pop('email', None)
    flash('Cleared stored name/email.')
    return redirect(url_for('index'))

# keep the dynamic route too (optional, nice for testing)
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name, current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True)
