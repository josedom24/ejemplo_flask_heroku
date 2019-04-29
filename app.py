import os
from flask import Flask, render_template,request,abort
from lxml import etree
import requests

app = Flask(__name__)	


@app.route('/',methods=["GET","POST"])
def inicio():
	return render_template("inicio.html")

@app.route('/temperatura',methods=["POST"])
def temperatura():
    key=os.environ["key"]
    ciudad=request.form.get("ciudad")
    payload = {'q': ciudad, 'mode': 'xml','units':'metric','APPID':key}
    r=requests.get('http://api.openweathermap.org/data/2.5/weather',params=payload)
    if r.status_code == 200:
	    doc = etree.fromstring(r.text.encode ('utf-8'))
	    temp=doc.xpath("temperature/@value")[0]
	    return render_template("temperatura.html",ciudad=ciudad,temperatura=temp)
    else:
        return render_template("temperatura.html",ciudad=ciudad,error=True)

port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)