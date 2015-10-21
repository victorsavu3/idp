from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('default.cfg')
app.config.from_envvar('CONFIG_FILE', silent=True)

db = SQLAlchemy(app)

import entities
from analyse import analyse

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
