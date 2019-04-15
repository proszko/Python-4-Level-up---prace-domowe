# app.py
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)
i=0


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method',methods = ['GET','POST','PUT','DELETE'])
def info():
    return request.method

@app.route('/show_data', methods =['POST'])
def postJson():
    content = request.get_json()
    return jsonify(content)
if __name__ == '__main__':
    app.run(debug=False)

@app.route('/pretty_print_name', methods =['POST'])
def pretty_names():
    dane=request.get_json()
    name=dane["name"]
    surename=dane["surename"]
    return f'Na imię mu {name}, a nazwisko jego {surename}'


@app.route('/counter', methods=['GET','POST','PUT','DELETE'])
def count():
    global i
    i=i+1
    return f'{i}'
