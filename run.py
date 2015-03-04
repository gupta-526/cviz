import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from werkzeug import SharedDataMiddleware
from werkzeug import secure_filename


UPLOAD_FOLDER="/"

ALLOWED_EXTENSIONS='json'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule('/uploads/myFiles', 'zoomable',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#Keeps Flask from swallowing error messages
app.config['PROPAGATE_EXCEPTIONS']=True

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():

	
    return render_template("index.html" )
	
@app.route("/zoomable.html", methods=["GET", "POST"])
def zoomable():

    file = request.files['myFiles']
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
    
    return render_template("zoomable.html", title=request.form['title'], subA=request.form['subjectA'], 
                            subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                            colorA=request.form['aColor'], colorB=request.form['bColor'], 
                            reqFile=url_for('zoomable',
                                    filename=filename))
	
if __name__ == '__main__':
	app.run()