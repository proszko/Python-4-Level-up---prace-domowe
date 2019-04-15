import os

from flask import Flask, abort, render_template, request, Response, json, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker


import models
from models import Base

DATABASE_URL = os.environ['DATABASE_URL']

#engine = create_engine("postgresql://postgres:postgres@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/artists", methods=["GET", "PATCH"])
def artists():
    if request.method == "GET":
        return get_artists()
    elif request.method == "PATCH":
        return patch_artist()
    abort(405)


def get_artists():
    artists = db_session.query(models.Artist).order_by(models.Artist.name)
    return "<br>".join(
        f"{idx}. {artist.name}" for idx, artist in enumerate(artists)
    )


# Aaron Goldberg , 202
def patch_artist():
    data = request.json
    artist_id = data.get("artist_id")
    new_name = data.get("name")
    if artist_id is None:
        abort(404)
    artist = (
        db_session.query(models.Artist)
        .filter(models.Artist.artist_id == artist_id)
        .with_for_update()
        .one()
    )
    artist.name = new_name
    db_session.add(artist)
    db_session.commit()
    return "OK"


@app.route("/albums")
def get_albums():
    albums = db_session.query(models.Album).order_by(models.Album.title)
    return render_template("albums.html", albums=albums)


@app.route("/playlists")
def get_playlists():
    playlists = db_session.query(models.Playlist).order_by(
        models.Playlist.name
    )
    return render_template("playlists.html", playlists=playlists)


def serialize_track(record):
    data={}
    data['track_id']=str(record.track_id)
    data['name']=str(record.name)
    data['album_id']=str(record.album_id)
    data['media_type_id']=str(record.media_type_id)
    data['genre_id']=str(record.genre_id)
    data['composer']=str(record.composer)
    data['milliseconds']=str(record.milliseconds)
    data['bytes']=str(record.bytes)
    data['unit_price']=str(record.unit_price)
    return data

def serialize_artist(record):
    data={}
    data['artist_id']=str(record.artist_id)
    data['name']=str(record.name)
    return data


@app.route("/longest_tracks")
def longest_tracks():
    try:
        tracks = (db_session.query(models.Track).order_by(models.Track.milliseconds.desc()).limit(10).all())
    except:
        abort(503)
    rdata=[]
    for thing in tracks:
        rdata.append(serialize_track(thing))
    return Response(json.dumps(rdata),200)
        
@app.route("/longest_tracks_by_artist")
def longest_tracks_by_artist():
    try:
        artist=request.args.get('artist')
        tracks = (
        db_session.query(models.Track)
        .join(models.Album)
        .join(models.Artist)
        .filter(models.Artist.name == artist)
        .order_by(models.Track.milliseconds.desc())
        .limit(10)
        .all()
        )
    except:
        abort(503)
    rdata=[]
    for thing in tracks:
        rdata.append(serialize_track(thing))
    if len(rdata) == 0:
        return Response ("No such arist found in database",404)
    
    return Response(json.dumps(rdata),200)

@app.route("/artists",methods=['POST'])
def add_artist():
    if request.method=='POST':
        data=request.get_json()
        try:
            new_name=data['name']   
            if not isinstance(new_name,str):
                abort(400)
            if not len(data)==1:
                abort(400)
        except KeyError:
            abort(400)
        new_artist = models.Artist(name=new_name)
        db_session.add(new_artist)
        db_session.commit()
        serialized=serialize_artist(new_artist)
        return Response(json.dumps(serialized),200)
        

@app.route('/count_songs')
def count_songs():
    original_artists=request.args.get('artist')
    try:
        artists=original_artists.split(',')
    except:
        abort(404)
        
    non_zero_flag=False
    
    to_send={}
    for artist_entry in artists:
        no_of_tracks=(
        db_session.query(func.count(models.Track.track_id))
        .join(models.Album)
        .join(models.Artist)
        .filter(models.Artist.name==artist_entry).scalar()
        )
        to_send[artist_entry]=no_of_tracks
        if no_of_tracks !=0 and non_zero_flag==False:
            non_zero_flag=True

    if non_zero_flag==False:
        abort(404)
    return jsonify(to_send)

if __name__ == "__main__":
    app.run(debug=True)
