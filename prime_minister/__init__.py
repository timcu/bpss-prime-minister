import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap                          # EXTRA


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)                                             # EXTRA

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
        return render_template('list_minister.html', page_title="Prime Ministers")

    from . import db
    db.init_app(app)

    return app

