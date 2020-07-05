#!/usr/bin/env bash
pip install -r requirements.txt
flask db migrate
flask db upgrade
npm start
