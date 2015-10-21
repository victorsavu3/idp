import importlib
import os
import sys
import analysis

from app import app, db
import git
import entities

def getModuleNames():
    return [ f for f in os.listdir('analysis') if os.path.isfile(os.path.join('analysis',f)) and f.endswith('.py') ]

def getModules():
    return [ importlib.import_module('analysis.' + f[:-3]) for f in getModuleNames() ]

modules = getModules()

def analyse(repository, branch):
    repodir = os.path.join(app.config['ANALYSIS_CLONE_FOLDER'], repository)

    if not os.path.isdir(repodir):
        url = 'git@' + app.config['GITOLITE_DOMAIN'] + ':feedback/' + repository

        git.Repo.clone_from(url, repodir)

    repo = git.Repo(repodir)
    repo.git.checkout(branch)
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
