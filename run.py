import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import current_app
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
    #print current_app.name
    
    #app.config['SERVER_NAME']='http://webapp-kumarlab.rhcloud.com:8080'
    app.config['PROPAGATE_EXCEPTIONS']=True
    app.config['UPLOAD_FOLDER'] = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'uploads/')
    #app.config['UPLOAD_FOLDER'] ='Users/purnimakumar/Documents/VisualModelApp/uploads/'
    app.config['ALLOWED_EXTENSIONS']=set(['json','jpg','jpeg'])
    #files=UploadSet('files',FILE)   
    #url=url_for(['UPLOAD_FOLDER']);
    #print "url for upload folder= "%url;
    app.add_url_rule('/upload', '/zoomable',
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
#         imageType=request.form['imageType']
#     #     print type(imageType)
#         if(imageType=='simple'):
#             app.add_url_rule('/uploads/myFiles', 'simple',
#                        build_only=True) 
#              return redirect('/simple')
#         else:
#              app.add_url_rule('/uploads/myFiles', 'zoomable',
#                        build_only=True) 
#              return redirect('/zoomable')

    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files['myFiles']
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('zoomable(filename)'))
        # return redirect('zoomable')
   
    # @app.route('/uploads/<filename>')
#     def uploaded_file(filename):
#         return send_from_directory(app.config['UPLOAD_FOLDER'],filename)    

    @app.route("/zoomable", methods=["GET", "POST"])
    def zoomable(filename):


        return render_template("zoomable.html", title=request.form['title'], subA=request.form['subjectA'], 
                                subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                                colorA=request.form['aColor'], colorB=request.form['bColor'], 
                                reqFile=os.path.join(aap.config['UPLOAD_FOLDER'],upload()))

    @app.route("/simple", methods=["GET","POST"])
    def simple(filename):
    
        return render_template("simple.html", title=request.form['title'], subA=request.form['subjectA'], 
                                subB=request.form['subjectB'], neutralColor=request.form['nColor'], 
                                colorA=request.form['aColor'], colorB=request.form['bColor'], 
                                reqFile=os.path.join(aap.config['UPLOAD_FOLDER'],upload()))
if __name__ == '__main__':
    app.debug=true
    #app.run(host='0.0.0.0', port=int("5000"))
    app.run()
