# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Counter(Base):
    __tablename__ = 'counter'

    counter_id = Column(Integer, primary_key=True, server_default=text("nextval('artist_artist_id_seq'::regclass)"))
    i = Column(Integer)
