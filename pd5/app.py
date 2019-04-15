import os

from flask import Flask, abort, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models import Base

DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_engine("postgresql://postgres:postgres@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



@app.route('/counter')
def countering():
    current_count = (
    db_session.query(models.Counter)
    .filter(models.Counter.counter_id == 1)
    .one()
    )
    current_count.i=current_count.i+1
    db_session.add(current_count)
    db_session.commit()
    return f'{current_count.i}'

    



if __name__ == "__main__":
    app.run(debug=False)
