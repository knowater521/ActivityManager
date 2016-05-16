from web import app, baseurl
from flask import render_template
from ..Model.database import Activities


@app.route('/')
def index():
    return render_template('index/index.html')


@app.route(baseurl)
def activity_chosen():
    acts = Activities.query.order_by(Activities.rank).all()
    return render_template('index/chosen_page.html', acts=acts)


app.add_url_rule(baseurl + '/', 'activity_chosen2', activity_chosen)
