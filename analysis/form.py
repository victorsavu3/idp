import os
import csv

from app import app

from flask import request, jsonify, render_template

def analyse(repository, branch, diff, repo, repodir):
    os.makedirs(os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'form', repository, branch), exist_ok=True)
    for form in os.listdir(os.path.join(repodir, 'form')):
        resultname = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'form', repository, branch, form)
        with open(resultname, 'w+') as result:
            with open(os.path.join(repodir, 'form', form), 'r') as source:
                sourcereader = csv.reader(source, dialect='excel')
                resultwriter = csv.writer(result, dialect='excel')

                resultwriter.writerows(sourcereader)

def data(repository, branch):
    form = request.args.get('form')

    if form is None:
        forms = [form for form in os.listdir(os.path.join(repodir, 'form'))]

        return jsonify(forms)
    else:
        formresult = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'form', repository, branch, form)

        with open(formresult, 'r') as source:
            return source.read()

def render(repository, branch):
    form = request.args.get('form')

    if form is None:
        forms = [form for form in os.listdir(os.path.join(repodir, 'form'))]

        return render_template('forms.html', forms=forms)
    else:
        formresult = os.path.join(app.config['ANALYSIS_DATA_FOLDER'], 'form', repository, branch, form)

        with open(formresult, 'r') as source:
            sourcereader = csv.reader(source, dialect='excel')

            return render_template('forms.html', data=sourcereader)
