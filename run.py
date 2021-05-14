#-*- coding: utf-8 -*-
from flask import Flask,render_template,request,send_file
import datetime, os, imgkit, glob, re, json


with open('setting.json') as json_file:
    setting_data = json.load(json_file)

app = Flask(__name__)
@app.route('/')
def main():
    if len(os.listdir("imgmaking/htmlforimg")) >= 30:
        for i in glob.glob("imgmaking/htmlforimg/*"): 
            os.remove(i)
        for i in glob.glob("imgmaking/imgs/*"):
            os.remove(i)
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

    filename = "/%s_%d"%(str(Thistime)[:11],
    len(os.listdir("imgmaking/htmlforimg"))+1)
    with open("imgmaking/htmlforimg/"+filename+".html","w",encoding="UTF-8") as f:
        f.write(cssstr + html_output)
    options = {
        'format': 'png',
        'quality':'100',
        'encoding':"UTF-8",
        'crop-h':'500',
        'crop-w':'500',

        }
    imgkit.from_file(setting_data['pathForImgkit']+"imgmaking/htmlforimg"+filename+".html",
    setting_data['pathForImgkit']+"imgmaking/imgs"+filename+".png",options=options,)
    return  send_file("imgmaking/imgs"+filename+".png",
                     mimetype='image/png',
                     attachment_filename=filename[1:]+".png",# 다운받아지는 파일 이름. 
                     as_attachment=True)
if __name__ == "__main__":
	app.run(host="0.0.0.0",port="80")
