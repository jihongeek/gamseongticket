#-*- coding: utf-8 -*-
from flask import Flask,render_template,request
import datetime
import re
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('template.html')

@app.route('/maketicket',methods={'POST'})
def maketicket():
    p = re.compile("[.].+")
    dt= datetime.datetime.now()
    dt= p.sub("",str(dt))
    Thistime = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    video_title = request.form['video-title']
    platform = request.form['platform']
    people = request.form['people']

    return render_template('ticket.html',
        Thistime=Thistime,
        video_title=video_title,
        platform=platform,
        people=people
        )
