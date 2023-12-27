import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Session
import pandas as pd
from typing import List

CONNECTION_STRING = "postgresql://doadmin:AVNS_4894TZ9zuWd4e4qmh5Y@db-postgresql-nyc3-57581-do-user-13892079-0.c.db.ondigitalocean.com:25060/Mneme?sslmode=require"

class Base(DeclarativeBase): 
    pass

class Request(Base):
    __tablename__ = "shorturl"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    resource_name = sa.Column(sa.String)
    request_method = sa.Column(sa.String)
    request_date = sa.Column(sa.DateTime)
    request_uri = sa.Column(sa.DateTime)
    ip = sa.Column(sa.String)

def write(item: dict) -> dict:
    r = Request(**item)
    engine = sa.create_engine(CONNECTION_STRING) 
    with Session(bind=engine) as session:
        session.add(r)
        session.commit()
