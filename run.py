import os
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

#Keeps Flask from swallowing error messages
app.config['PROPAGATE_EXCEPTIONS']=True

@app.route('/')
@app.route("/index", methods=["GET", "POST"])
def index():
    notes={"name":"First",
            "author":"Niharika",
            "content":"Text from content field"
        }
    return render_template("index.html",notes = notes)
    
#def insult():
    #return "Hello!"
#@app.route("/hello/<name>")
#def input(name=None):
    #return render_template('inputData.html')

if __name__ == '__main__':
    app.run()