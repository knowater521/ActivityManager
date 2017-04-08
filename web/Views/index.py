from web import app, baseurl
from flask import render_template,redirect,url_for
from ..Model.database import Activities



@app.route('/')
def index():
    acts = Activities.query.filter_by(hide=False).order_by(Activities.rank).all()
    if len(acts) == 1:
    	return redirect(url_for('reg',activity=acts[0].activity_name))
    return render_template('index/chosen_page.html', acts=acts)



def no_base_url():
    return redirect(url_for('index'))

if baseurl != '':
    app.add_url_rule('/',view_func=no_base_url)
