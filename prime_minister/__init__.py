import os

from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from datetime import date
from . import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'pm.sqlite'),    # change db name
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # EXTRA: Add routes to web pages

    @app.route('/')
    def index():
        return render_template('index.html', page_title="Beginner's Python Web Application")

    @app.route('/persons/')
    def view_persons():
        return render_template('list_person.html', page_title="People in database")

    @app.route('/prime_ministers/')
    def view_prime_ministers():
        ministry = "Prime Minister"
        page_title = ministry + 's'
        pm_db = db.get_db()
        sql = """select distinct p.id, p.vc_common_name, p.vc_surname, p.date_birth, p.vc_birth_place, p.date_death 
                from tbl_person p inner join tbl_ministry m on p.id=m.id_person 
                where m.vc_ministry=?
                order by p.vc_surname asc, p.vc_common_name asc"""
        ministers = pm_db.execute(sql, (ministry,)).fetchall()
        return render_template('list_minister.html', ministers=ministers, ministry=ministry, page_title=page_title)

    # Filters

    from . import db
    db.init_app(app)

    return app
