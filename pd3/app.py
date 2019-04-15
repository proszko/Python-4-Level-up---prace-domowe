# app.py
from flask import Flask
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask import Response
from functools import wraps
from flask import render_template
from uuid import uuid4, UUID

app = Flask(__name__)
app.secret_key = 'zpry sa super'
app.trainz={}
app.population=0

@app.route('/')
def root():
    return 'I like trains'


def requires_user_session(destination):
    def fake_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not session.get('login'):            #Brak sesji
                return redirect(url_for(destination))
            return func(*args, **kwargs)
        return inner
    return fake_decorator



@app.route('/hello')
@requires_user_session('login')
def hello():
    return render_template('hellohellohello.html', username=session['login'])


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method=='POST' and request.authorization.username=='TRAIN' and request.authorization.password=='TuN3L':
        session['login']='TRAIN'
        session['password']='TuN3L'
        return redirect(url_for('hello'))
    else:
        return Response('Zle dane',401)

@app.route('/trains',methods=['GET','POST'])
@requires_user_session('login')
def trains():
    if request.method=='POST':
        data=request.get_json()
        app.population+=1
        new_train={
            'who': data.get('who'),
            'where': data.get('where'),
            'trucks': data.get('trucks'),
            'locomotive': data.get('locomotive'),
            'date': data.get('date')
        }
        train_id=str(uuid4())
        app.trainz[train_id]=new_train

        return redirect(url_for('trainyard',train_id=train_id, format='json'))
    if request.method=='GET':
        return jsonify(app.trainz)

@app.route('/trains/<train_id>',methods=['GET','DELETE'])
@requires_user_session('root')
def trainyard(train_id):
    if request.method=='GET':
        return jsonify(app.trainz[train_id])
    if request.method=='DELETE':
        del app.trainz[train_id]
        return '',204
    

@app.route('/logout',methods=['GET','POST'])
@requires_user_session('login')
def logout():
    if request.method=='GET':
        return redirect(url_for('root'))
    del session['login']
    del session['password']                    
    return redirect(url_for('root'))
           
           

if __name__=='__main__':
    app.run(debug=False)


