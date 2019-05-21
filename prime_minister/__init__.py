import os

from flask import Flask, render_template, abort, request
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

    # Utility functions

    def age(birthday, age_day=date.today()):
        """Returns person's age at age_day given their birthday
        Checks if they have already had their birthday in final year
        """
        birthday_in_age_year = date(year=age_day.year, month=birthday.month, day=birthday.day)
        if birthday_in_age_year > age_day:
            return age_day.year - birthday.year - 1
        else:
            return age_day.year - birthday.year

    # Routes to web pages

    @app.route('/')
    def index():
        return render_template('index.html', page_title="Beginner's Python Web Application")

    @app.route('/person/<id_person>')
    def view_person(id_person):
        if not id_person:
            abort(404)
        pm_db = db.get_db()
        person = pm_db.execute('select * from tbl_person where id=?', (id_person,)).fetchone()
        if not person:
            abort(404)
        if person['date_death'] and person['date_birth']:
            person = dict(person)  # convert to dict as sqlite3.Row does not support item assignment
            person['age_death'] = age(person['date_birth'], person['date_death'])
        sql = """select m1.*, m2.date_start as date_end
            from tbl_ministry m1 left join tbl_ministry m2 on m1.id_next=m2.id
            where m1.id_person=?
            order by m1.date_start asc"""
        ministries = pm_db.execute(sql, (id_person,)).fetchall()
        sql = """select * from tbl_recreation where id_person=?"""
        recreations = pm_db.execute(sql, (person['id'],)).fetchall()
        return render_template('view_person.html', person=person, ministries=ministries, recreations=recreations, page_title="View person")

    @app.route('/persons/', methods=('GET', 'POST'))
    def view_persons():
        def sql_search_str(form_search_str):
            if form_search_str is None or len(form_search_str.strip()) == 0:
                return '%'
            else:
                return '%' + form_search_str.strip() + '%'

        pm_db = db.get_db()
        if request.method == 'POST':
            given_name = sql_search_str(request.form['given-name'])
            surname = sql_search_str(request.form['surname'])

            sql = """select distinct p.id, p.vc_common_name, p.vc_given_names, p.vc_surname, p.date_birth, p.vc_birth_place, p.date_death 
                    from tbl_person p
                    where (p.vc_common_name like :gn or p.vc_given_names like :gn) and p.vc_surname like :sn
                    order by p.vc_surname asc, p.vc_common_name asc"""
            persons = pm_db.execute(sql, {"gn": given_name, "sn": surname}).fetchall()
        else:
            persons = None
        return render_template('list_person.html', persons=persons, page_title="People in database")

    def view_ministers(ministry="Prime Minister", page_title=None):
        if page_title is None:
            page_title = ministry + 's'
        pm_db = db.get_db()
        sql = """select distinct p.id, p.vc_common_name, p.vc_surname, p.date_birth, p.vc_birth_place, p.date_death 
                from tbl_person p inner join tbl_ministry m on p.id=m.id_person 
                where m.vc_ministry=?
                order by p.vc_surname asc, p.vc_common_name asc"""
        ministers = pm_db.execute(sql, (ministry,)).fetchall()
        return render_template('list_minister.html', ministers=ministers, ministry=ministry, page_title=page_title)

    @app.route('/prime_ministers/')
    def view_prime_ministers():
        return view_ministers("Prime Minister")

    @app.route('/deputy_prime_ministers/')
    def view_deputy_prime_ministers():
        return view_ministers("Deputy Prime Minister")

    # Filters

    @app.template_filter('date_format')
    def date_format_filter(value, date_format="%d-%b-%Y"):
        try:
            return value.strftime(date_format)
        except AttributeError:
            return value

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
