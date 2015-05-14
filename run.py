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
    
    app.config['DEBUG']=True
    app.config['TRAP_BAD_REQUEST_ERRORS']=True
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY','harryPotterAndTheGobletOfFire')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'uploads/')
    #app.config['UPLOAD_FOLDER'] ='Users/purnimakumar/Documents/VisualModelApp/uploads/'
    app.config['ALLOWED_EXTENSIONS']=set(['json'])
    app.add_url_rule('/getModel', 'simple',build_only=True)
    app.add_url_rule('/getModel', 'zoomable',build_only=True)
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
    
    @app.route('/upload', methods=['POST'])
    def upload():
      file = request.files['myFiles']
      filename=""
      if file and allowed_file(file.filename):
          filename=secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return  path
    
    @app.route('/getModelType', methods=['GET','POST'])  
    def getModelType():
        imageType=request.form['imageType']
        # filename=upload()
        if(imageType=='simple'):
   
            return render_template("simple.html",title=request.form['title'],
                                   subA=request.form['subjectA'],
                                   subB=request.form['subjectB'],
                                   neutralColor=request.form['nColor'],
                                   colorA=request.form['aColor'],
                                   colorB=request.form['bColor'],
                                   reqFile=upload())
        elif(imageType=='zoomable'):

            return render_template("zoomable.html",title=request.form['title'],
                                       subA=request.form['subjectA'],
                                       subB=request.form['subjectB'],
                                       neutralColor=request.form['nColor'],
                                       colorA=request.form['aColor'],
                                       colorB=request.form['bColor'],
                                       reqFile=upload())


        
        

    # @app.route('/zoomable', methods=["GET","POST"])
#     def zoomable():
#         title=request.form['title']
#         subA=request.form['subjectA']
#         subB=request.form['subjectB']
#         neutralColor=request.form['nColor']
#         colorA=request.form['aColor']
#         colorB=request.form['bColor']
#         reqFile=''
#         return render_template("zoomable.html",title=title,subA=subA,
#                                 neutralColor=neutralColor,colorA=colorA,colorB=colorB,
#                                 reqFile=reqFile)
# 
#     @app.route('/simple', methods=["GET","POST"])
#     def simple():
#         title=request.form['title']
#         subA=request.form['subjectA']
#         subB=request.form['subjectB']
#         neutralColor=request.form['nColor']
#         colorA=request.form['aColor']
#         colorB=request.form['bColor']
#         reqFile=''    
#         return render_template("simple.html",title=title,subA=subA,
#                                 neutralColor=neutralColor,colorA=colorA,colorB=colorB,
#                                 reqFile=reqFile)

if __name__ == '__main__':
    app.debug = True
    #app.run(host='0.0.0.0', port=int("5000"))
    app.run()
