from flask import Flask #importing Flask class from flask module

app = Flask(__name__) 

@app.route('/') 
@app.route('/home')
def hello_world(): 
    return "<h1><b>Hello world</b></h1>"+__name__

@app.route('/about') 
def about(): 
    return "<h1><b>Hello world</b></h1>"+__name__

if __name__=="__main__": 
    app.run(debug=True)