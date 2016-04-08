import sqlalchemy
print (sqlalchemy.__version__ )
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Enum, SmallInteger, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timedelta
import pandas as panda                ##require python -m pip install pandas
import numpy as np
import sys
import time
from pandas.core import format

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String(25))
     fullname = Column(String(25))
     password = Column(String(25))

     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)


##print(User.__table__ )

'''ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user.name)
print(ed_user.password)
print(str(ed_user.id))'''
engine = create_engine("postgresql://postgres:P@nd0s+@vps234953.ovh.net:5432/velovDB", echo=True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
##Session.configure(bind=engine)  # once engine is available

'''ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
our_user = session.query(User).filter_by(name='ed').first()
print (our_user)
ed_user is our_user
print("here")
session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'),User(name='mary', fullname='Mary Contrary', password='xxg527'),User(name='fred', fullname='Fred Flinstone', password='blah')])
ed_user.password = 'f8s7ccs'
print(session.dirty)
print(session.new)
session.commit()'''
'''for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)'''
#print(str(session.query(Objectives_aggregations).count()))

df=panda.DataFrame()
df=panda.read_json(path_or_buf="https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&outputformat=GEOJSON&maxfeatures=30&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171")
iteration=0

for row in df.get_values():
    print (row)

#print (df[0].get('geometry'))
'''
for occurence in df :
    print(occurence)
    print(occurence.get('geometry').get('coordinates')[0])
    print(occurence.get('geometry').get('coordinates')[1])
    print(occurence.get('properties').get('last_update'))

print(df)
print(df.iloc(10))
print(df.to_panel())'''




