from web import app
from web import baseurl


@app.route(baseurl + '/admin/home')
def admin_home():
    return "under construction"
