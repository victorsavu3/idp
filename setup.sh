#!/bin/bash

virtualenv-3.4 virtualenv

. activate.sh

pip install Flask-SQLAlchemy gitpython flask pycrypto chartkick

