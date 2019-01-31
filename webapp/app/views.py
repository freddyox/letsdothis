from flask import render_template, url_for
from app import app
from flask import request
from flask_wtf import FlaskForm
from wtforms import SelectField
import pandas as pd
import analysis
from event_handler import event_handler

@app.route('/')
@app.route('/index')
def index():
    d = event_handler()
    events = d.get_events('Mar')
    return render_template("index.html", events=events)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/output')
def output():
    age_type    = str(request.args.get('age'))
    gender_type = str(request.args.get('gender'))
    race_type   = str(request.args.get('race'))
    event_type  = str(request.args.get('event'))

    print(' age = %s \n sex = %s \n race = %s \n evt = %s' %
          (age_type, gender_type, race_type, event_type))
    
    results = analysis.predict(age_type, gender_type, race_type, event_type)
    betax, score = results[0], results[1]
   
    return render_template("output.html", betax=betax, score=score)
