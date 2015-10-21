import app

db = app.db

from repo import RepoManager

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    analysis = db.relationship('Analysis', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def create(self):
        RepoManager.initRepos(self.name)

    def __repr__(self):
        return '<Repo %r>' % self.name

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(80))
    commit = db.Column(db.String(80))

    def __init__(self, repo, branch):
        self.branch = branch
        self.repo = repo
        self.commit = 'initial_commit'

    repo = db.Column(db.Integer, db.ForeignKey('repository.id'))
