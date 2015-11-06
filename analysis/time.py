import os
import csv

from app import app

from flask import request, jsonify, render_template

def analyse(repository, branch, diff, repo, repodir):
    timeresult = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'time', repository, branch, 'timing.csv')
    os.makedirs(os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'time', repository, branch), exist_ok=True)
    with open(timeresult, 'w+') as result:
        with open(os.path.join(repodir, 'time', 'timing.csv'), 'r') as source:
            sourcereader = csv.reader(source, dialect='excel')
            resultwriter = csv.writer(result, dialect='excel')

            resultwriter.writerows(sourcereader)

def data(repository, branch):
    timeresult = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'time', repo, branch, 'timing.csv')

    with open(timeresult, 'r') as source:
        return source.read()

def render(repository, branch):
    timeresult = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'form', repository, branch, 'timing.csv')

    with open(timeresult, 'r') as source:
        sourcereader = csv.reader(source, dialect='excel')

        return render_template('time.html', data=sourcereader)
