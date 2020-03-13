#-*- coding: utf-8 -*-
from flask import Flask,render_template,request,send_file
import datetime
import re
import io
import os
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
    place = request.form['place']
    cssfile = open("static/styles/ticket.css","r")
    cssstr = "<style>\n" + cssfile.read() + "\n</style>\n"
    html_output = render_template(
            'ticket.html',
            Thistime=Thistime,
            video_title=video_title,
            platform=platform,
            people=people,
            place=place
            ) 
    with open("imgmaking/htmlforimg/%s_%d.html"
    %(str(Thistime)[:11],
    len(os.listdir("imgmaking/htmlforimg"))+1),"w",
    encoding="UTF-8") as f:
        f.write(cssstr + html_output)
    return cssstr + html_output
app.run(debug=True)