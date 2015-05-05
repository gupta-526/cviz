import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from werkzeug import secure_filename
 
 #get the upload function in a separate function so that zoomable isnt doing so many things
 #a different form for the upload files?? if so how to link the rest of the data you get from index
 #pass file name/url/path to the d3.js location required. 




app = Flask(__name__)
with app.app_context():
    #Keeps Flask from swallowing error messages
    app.config['SERVER_NAME']='webapp-kumarlab.rhcloud.com:8080'
    app.config['PROPAGATE_EXCEPTIONS']=True
    app.config['UPLOAD_FOLDER'] = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'uploads/')
    url=url_for(['UPLOAD_FOLDER']);
    # print "url for upload folder= "%url;

    app.config['ALLOWED_EXTENSIONS']='json'

    app.add_url_rule('/uploads/myFiles', 'zoomable',
                      build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/':  app.config['UPLOAD_FOLDER']
    })

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



    @app.route("/")
    @app.route("/index", methods=["GET", "POST"])
    def index():

    
        return render_template("index.html" )

    # def getModelType():
    #     model=request.form['simple']
    #     if(model=='simple')
    #         return redirect('/simple')
    #     else 
    #         return redirect('/zoomable')

    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files['myFiles']
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # url2= url_for('uploaded_file', filename=filename) 
    #         print "url for upload folder= "%url2;
        return url_for('uploaded_file', filename=filename) 

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)    
    
    @app.route("/zoomable", methods=["GET", "POST"])
    def zoomable():

   
        return render_template("zoomable.html", title=request.form['title'], subA=request.form['subjectA'], 
                                subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                                colorA=request.form['aColor'], colorB=request.form['bColor'], reqFile=upload())

    @app.route("/simple", methods=["GET","POST"])
    def simple():
        return render_template("simple.html", title=request.form['title'], subA=request.form['subjectA'], 
                                subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                                colorA=request.form['aColor'], colorB=request.form['bColor'], reqFile=upload())
    if __name__ == '__main__':
        app.run()