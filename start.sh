#!/usr/bin/env bash
pip install -r requirements.txt
npm install
flask db migrate
flask db upgrade
npm start
