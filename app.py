from flask import Flask, request, Blueprint, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import chartkick

app = Flask(__name__)

app.config.from_pyfile('default.cfg')
app.config.from_envvar('CONFIG_FILE', silent=True)

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

db = SQLAlchemy(app)

app.jinja_env.globals.update(max=max)

import entities
from analyse import analyse

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/repositories')
def repositories():
    repositories = entities.Repository.query.all()

    return render_template('repositories.html', repositories=repositories)

@app.route('/analyse')
def analyse_cb():
    repo = request.args.get('repository')
    branch = request.args.get('branch')

    analyse(repo, branch)

    return 'Done'

@app.route('/repo/create')
def repo_create_cb():
    name = request.args.get('name')

    repo = entities.Repository(name)

    repo.create()

    db.session.add(repo)
    db.session.commit()

    return 'Done'

@app.route('/user/create')
def user_create_cb():
    name = request.args.get('name')

    user = entities.User(name)

    key = user.generateKey()
    user.create()

    db.session.add(user)
    db.session.commit()

    return key
