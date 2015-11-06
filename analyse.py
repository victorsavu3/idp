import importlib
import os
import sys
import analysis

from app import app, db
from flask import request

import git
import entities

from functools import partial

def getModuleNames():
    return [ f for f in os.listdir('analysis') if os.path.isfile(os.path.join('analysis',f)) and f.endswith('.py') ]

def getModules():
    return [ importlib.import_module('analysis.' + f[:-3]) for f in getModuleNames() ]

def callRenderingFunction(fct):
    repository = request.args.get('repository')
    branch = request.args.get('branch')

    return fct(repository, branch)

def addRoutes(modules):
    for module in modules:
        data = partial(callRenderingFunction, module.data)
        render = partial(callRenderingFunction, module.render)

        data.methods = ['GET']
        render.methods = ['GET']

        data.provide_automatic_options = False
        render.provide_automatic_options = False

        app.add_url_rule('/analysis/' + module.__name__ + '/data', module.__name__ + '_data', data)
        app.add_url_rule('/analysis/' + module.__name__ + '/render', module.__name__ + '_render', render)

modules = getModules()

addRoutes(modules)

def analyse(repository, branch):
    repodir = os.path.join(app.config['ANALYSIS_CLONE_FOLDER'], repository)

    if not os.path.isdir(repodir):
        url = 'git@' + app.config['GITOLITE_DOMAIN'] + ':feedback/' + repository

        git.Repo.clone_from(url, repodir)

    repo = git.Repo(repodir)
    repo.git.fetch()
    repo.git.checkout('origin/' + branch)
    repo.remotes.origin.pull()

    repoTable = entities.Repository.query.filter_by(name=repository).first()

    now = repo.head.commit

    analysisStatus = repoTable.analysis.filter_by(branch=branch).first()

    if analysisStatus is None:
        analysisStatus = entities.Analysis(repoTable.id, branch)
        db.session.add(analysisStatus)
        db.session.commit()

    diff = now.diff(analysisStatus.commit)

    for module in modules:
        module.analyse(repository, branch, diff, repo, repodir)

    analysisStatus.commit = str(now)

    db.session.commit()
