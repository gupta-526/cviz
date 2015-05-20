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
    app.config['ALLOWED_EXTENSIONS']=set(['json','txt'])
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
          path=os.path.join('/uploads', filename)
      return  path
    
    
    
    def mtable_to_json(mg_abundance):
#     """
#     Convert a list of functional abundance data (level1,level2,level3,level4,abundance) into 
#     a hierarchical JSON file: {name: ..., children: [name:..., size:...]}
#     """
    hierarchy = {'name': 'metagenome', 'children':[]}
    for entry in mg_abundance:
        L1_idx = -1
        lvl1, lvl2, lvl3, lvl4, count = entry[0], entry[1], entry[2], entry[3], float(entry[4])
        for i, c in enumerate(hierarchy['children']):
            if c['name'] == lvl1:
                L1_idx = i
                break
        else:
            hierarchy['children'].append({'name':lvl1, 
                                          'children':[{'name':lvl2, 
                                                       'children':[{'name':lvl3, 
                                                                    'children':[{'name':lvl4, 'size':count}]}]}]})
            continue
        if L1_idx > -1:
            L2_idx = -1
            for j, c in enumerate(hierarchy['children'][L1_idx]['children']):
                if c['name'] == lvl2:
                    L2_idx = j
                    break
            else:
                hierarchy['children'][L1_idx]['children'].append({'name': lvl2, 
                                                                  'children':[{'name':lvl3, 
                                                                               'children':[{'name':lvl4, 'size':count}]}]})
                continue
        if L2_idx > -1:
            for c in hierarchy['children'][L1_idx]['children'][L2_idx]['children']:
                if c['name'] == lvl3:
                    c['children'].append({'name':lvl4, 'size':count})
                    break
            else:
                hierarchy['children'][L1_idx]['children'][L2_idx]['children'].append({'name': lvl3, 
                                                                                      'children':[{'name':lvl4, 'size':count}]})
        
    return hierarchy

    
    def process_fc_data(fc_lvl_fp, json_out_fp, delim='\t')
    # """
#     Takes a tab-delimited spreadsheet file as input with the f
#     """
    with open(fc_lvl_fp, 'rU') as in_f:
        fc_lvl_data = [line for line in csv.reader(in_f, delimiter=delim)][1:]

    with open(json_out_fp, 'w') as out_f:
        json.dump(mtable_to_json(fc_lvl_data), out_f)
        
    #method to render template using various variables from form and the filename+path
    @app.route('/getModelType', methods=['GET','POST'])  
    def getModelType():
        
        imageType=request.form['imageType']
        fileAfterConversion=process_fc_data(upload(),'temp.json',delim='\t')
        filename=secure_filename(fileAfterConversion.filename)
        fileAfterConversion.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # filename=upload()
        
        if(imageType=='simple'):
            fileAlias=upload()
            urlAlias=request.form['urlName']
            return render_template("simple.html",title=request.form['title'],
                                   subA=request.form['subjectA'],
                                   subB=request.form['subjectB'],
                                   nColor=request.form['nColor'],
                                   fillColor=request.form['fColor'],
                                   colorA=request.form['aColor'],
                                   colorB=request.form['bColor'],
                                   opacityRoot=request.form['opacity'],
                                   fontType=request.form['fontList'],
                                   reqFile='/uploads/filename')
        elif(imageType=='zoomable'):
            fileAlias=upload()
            urlAlias=request.form['urlName']
            return render_template("zoomable.html",title=request.form['title'],
                                       subA=request.form['subjectA'],
                                       subB=request.form['subjectB'],
                                       nColor=request.form['nColor'],
                                       fillColor=request.form['fColor'],
                                       colorA=request.form['aColor'],
                                       colorB=request.form['bColor'],
                                       opacityRoot=request.form['opacity'],
                                       fontType=request.form['fontList'],
                                       reqFile=upload())


if __name__ == '__main__':
    app.debug = True
    #app.run(host='0.0.0.0', port=int("5000"))
    app.run()
