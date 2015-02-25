import os
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

#Keeps Flask from swallowing error messages
app.config['PROPAGATE_EXCEPTIONS']=True

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method=='POST':
       title=request.form['title']
       subA=request.form['subjectA']
       subB=request.form['subjectB']
       lvZero=request.form['pfColor']
       neutralColor=request.form['nColor']
       colorA=request.form['aColor']
       colorB=request.form['bColor']	
	
    return render_template("index.html" )
	
@app.route("/zoomable.html", methods=["GET", "POST"])
def zoomable():
    if request.method=='POST':
       title=request.form['title']
       subA=request.form['subjectA']
       subB=request.form['subjectB']
       lvZero=request.form['pfColor']
       neutralColor=request.form['nColor']
       colorA=request.form['aColor']
       colorB=request.form['bColor']
       	    
    return render_template("zoomable.html" )
	

if __name__ == '__main__':
	app.run()