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

	
    return render_template("index.html" )
	
@app.route("/zoomable.html", methods=["GET", "POST"])
def zoomable():
  	    
    return render_template("zoomable.html", title=request.form['title'], subA=request.form['subjectA'], 
                            subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                            colorA=request.form['aColor'], colorB=request.form['bColor'], reqFile=request.files['myFiles'] )
	
if __name__ == '__main__':
	app.run()