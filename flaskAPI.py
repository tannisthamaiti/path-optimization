from flask import Flask,request,render_template, abort,json, redirect, url_for
from flask_cors import CORS
import convertJSON as cj
import astar as algo


app = Flask(__name__,template_folder="template")
CORS(app)

class Path:
    def __init__(self, key, name, lat, lng):
        self.key  = key
        self.lat  = lat
        self.lng  = lng


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/location_details', methods=['GET', 'POST'])
def home():
    #raw_input = request.args.get('pntdata').split(',')
    
    
    # inputSourceLoc = (float(raw_input[0]),float(raw_input[1]))
    # inputDestLoc = (float(raw_input[2]), float(raw_input[3]))
    
    if request.method == "POST":
        user = request.form["nm"]
        startL = request.form["sl"]
        endL = request.form["el"]
        return redirect(url_for("user", usr=user, sl=startL, el=endL))
    else:
        return render_template("login.html")
    
@app.route("/<usr>?<sl>&<el>")
def user(usr,sl,el):
    slat,slng = sl.split(",")
    elat,elng = el.split(",")
    inputSourceLoc = (slat,slng)
    inputDestLoc = (elat,elng)
    mappedSourceLoc = cj.getKNN(inputSourceLoc)
    mappedDestLoc = cj.getKNN(inputDestLoc)
    path = algo.aStar(mappedSourceLoc, mappedDestLoc)
    finalPath, cost = cj.getResponsePathDict(path, mappedSourceLoc, mappedDestLoc)
    
    
    # print("Cost of the path(km): "+str(cost))
    # print(finalPath[0]["lat"],finalPath[0]["lng"])
    labels=json.dumps(finalPath)
    
    return render_template('osmmap.html', path=finalPath, labels=labels)
    
    
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')