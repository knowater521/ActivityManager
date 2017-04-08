from web import app, baseurl
from flask import render_template, redirect, url_for
from ..Model.database import Activities


def index():
    acts = Activities.query.order_by(Activities.rank).all()
    return render_template('index/chosen_page.html', acts=acts)


app.add_url_rule(baseurl + '/', 'activity_chosen2', index)


def no_base_url():
    return redirect(url_for('index'))


if baseurl != '':
    app.add_url_rule('baseurl', view_func=index)
    app.add_url_rule('/', view_func=no_base_url)
else:
    app.add_url_rule('/', view_func=index)
