import os
from flask import Flask,session
from flask import render_template
from flask import request
from flask import redirect
from flask import current_app
from flask import url_for
from flask import flash
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from werkzeug import secure_filename


app = Flask(__name__)

with app.app_context():
    
    
    app.config['TRAP_BAD_REQUEST_ERRORS']=True
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY','harryPotterAndTheGobletOfFire')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'uploads/')
    #app.config['UPLOAD_FOLDER'] ='Users/purnimakumar/Documents/VisualModelApp/uploads/'
    app.config['ALLOWED_EXTENSIONS']='json'
    
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/uploads':  app.config['UPLOAD_FOLDER']
    })

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



    @app.route("/")
    @app.route("/index", methods=["GET", "POST"])
    def index():


        return render_template("index.html" )

 
    @app.route('/getModelType', methods=['GET','POST'])  
    def getModelType():
        imageType=request.form['imageType']
        filename=upload()
        if(imageType=='simple'):
#             app.add_url_rule('/getModelType/upload', 'simple',simple,
#                             build_only=True) 
            return redirect(url_for('simple',filename=filename))
        elif(imageType=='zoomable'):
#             app.add_url_rule('/getModelType/upload', 'zoomable',zoomable,
#                             build_only=True) 
            return redirect(url_for('zoomable',filename=filename))
    
    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files['myFiles']
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return os.path.join(app.config['UPLOAD_FOLDER'], filename)
        

    @app.route('/zoomable/<filename>', methods=["GET", "POST"])
    def zoomable(filename):
        return render_template("zoomable.html", title=request.form['title'], subA=request.form['subjectA'], 
                                subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                                colorA=request.form['aColor'], colorB=request.form['bColor'],
                                reqFile=filename)

    @app.route('/simple/<filename>', methods=["GET","POST"])
    def simple(filename):
    
        return render_template("simple.html", title=request.form['title'], subA=request.form['subjectA'], 
                                subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                                colorA=request.form['aColor'], colorB=request.form['bColor'], 
                                reqFile=filename)

if __name__ == '__main__':
    app.debug = True
    #app.run(host='0.0.0.0', port=int("5000"))
    app.run()
