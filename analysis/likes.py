import os
import csv

from app import app

from flask import request, jsonify, render_template

def analyse(repository, branch, diff, repo, repodir):
    resultname = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'likes', repository, branch)
    os.makedirs(os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'likes', repository), exist_ok=True)
    with open(resultname, 'w+') as result:
        resultwriter = csv.writer(result, dialect='excel')
        for fname in os.listdir(os.path.join(repodir, 'likes')):
            with open(os.path.join(repodir, 'likes', fname), 'r') as source:
                likes = int(source.readline())
                dislikes = int(source.readline())

                resultwriter.writerow([fname, likes, dislikes])

def data(repository, branch):
    resultname = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'likes', repository, branch)
    with open(resultname, 'r') as source:
        return source.read()

def render(repository, branch):
    resultname = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'likes', repository, branch)
    with open(resultname, 'r') as source:
        sourcereader = csv.reader(source, dialect='excel')

        return render_template('likes.html', data=sourcereader)
