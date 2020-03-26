#-*- coding: utf-8 -*-
from flask import Flask,render_template,request,send_file
import datetime
import re
import io
import os
import imgkit
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
    theme = request.form['theme']
    cssfile = open("static/styles/%s.css"%theme,"r")
    cssstr = "<style>\n" + cssfile.read() + "\n</style>\n"
    
    html_output = render_template(
            'ticket.html',
            Thistime=Thistime,
            video_title=video_title,
            platform=platform,
            people=people,
            place=place
            ) 

    filename = r"\%s_%d"%(str(Thistime)[:11],
    len(os.listdir("imgmaking/htmlforimg"))+1)
    with open("imgmaking/htmlforimg/"+filename+".html","w",encoding="UTF-8") as f:
        f.write(cssstr + html_output)

    path_wkthmltoimage = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe"
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
    options = {
        'format': 'png',
        'quality':'100',
        'encoding':"UTF-8",
        'crop-h':'500',
        'crop-w':'500',
        }
    imgkit.from_file(r"C:\develop\gamseongticket\imgmaking\htmlforimg"+filename+".html",
    r"C:\develop\gamseongticket\imgmaking\imgs"+filename+".png",config=config,options=options,)
    return  send_file(r"C:\develop\gamseongticket\imgmaking\imgs"+filename+".png",
                     mimetype='image/png',
                     attachment_filename=filename[1:]+".png",# 다운받아지는 파일 이름. 
                     as_attachment=True)
app.run(debug=True)