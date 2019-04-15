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
from flask import g
import sqlite3

DATABASE = 'chinook.db'
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()





@app.route('/')
def root():
    return "Out of my database!"

@app.route('/tracks',methods=['GET','POST'])
def trackings():
    db=get_db()
    if request.method=='GET':
        artist=request.args.get('artist')
        page_limit=request.args.get('per_page')
        page_offset=request.args.get('page')


        sql_command='SELECT tracks.name, artists.name from tracks JOIN albums ON tracks.albumid = albums.albumid JOIN artists on albums.artistid = artists.artistid'
        key_words={}
        if artist is not None:
            key_words['artist_name']=artist
            sql_command=sql_command+' WHERE artists.name = :artist_name'
        sql_command=sql_command+' ORDER BY tracks.name'
        if page_limit is not None:
            key_words['page_limit']=int(page_limit)
            sql_command=sql_command+' LIMIT :page_limit'
            if page_offset is not None:
                key_words['page_offset']=(int(page_offset)-1)*int(page_limit)
                sql_command=sql_command+' OFFSET :page_offset'
        sql_command=sql_command+' COLLATE NOCASE'
        
        data= db.execute(sql_command,key_words).fetchall()
        data2=[]
        for elee in data:
            data2.append(elee[0])
        
        return Response(jsonify(data2),200)
    
    if request.method=='POST':
        data=request.get_json()
        if 'album_id' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['album_id'],str):
#            return Response('Invalid data',400)
        
        if 'media_type_id' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['media_type_id'],int):
#            return Response('Invalid data',400)

        if 'genre_id' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['genre_id'],int):
#            return Response('Invalid data',400)
        
        if 'name' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['name'],str):
#            return Response('Invalid data',400)

        if 'composer' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['composer'],str):
#            return Response('Invalid data',400)

        if 'milliseconds' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['milliseconds'],int):
#            return Response('Invalid data',400)

        if 'bytes' not in data:
            return Response('Incomplete data',400)
#        if not isinstance(data['bytes'],int):
#            return Response('Invalid data',400)

        if 'price' not in data:
            return Response('Incomplete data',400)
        if not isinstance(data['price'],float):
            return Response('Invalid data',400)
        

        
        sql_command='INSERT INTO tracks (Name,Albumid,MediaTypeId,GenreId,Composer,Milliseconds,Bytes,UnitPrice) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        sql_keywords=(data['name'],data['album_id'],data['media_type_id'],data['genre_id'],data['composer'],data['milliseconds'],data['bytes'],data['price'],)

        db.execute(sql_command,(data['name'],data['album_id'],data['media_type_id'],data['genre_id'],data['composer'],data['milliseconds'],data['bytes'],data['price'],))
        return_data=db.execute('SELECT * FROM tracks where name = ?',(data['name'],)).fetchall()
        return jsonify(return_data)

@app.route('/genres')
def generic():
    db=get_db()
    sql_command='SELECT genres.name, count(*) from tracks INNER JOIN genres ON tracks.GenreId=genres.GenreId GROUP by genres.name ORDER BY genres.name'
    data=db.execute(sql_command).fetchall()
    data2={}
    for elee in data:
        data2[elee[0]]=elee[1]
   
    return jsonify(data2)
        



if __name__=='__main__':

    app.run(debug=True)
