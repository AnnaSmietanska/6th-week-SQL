import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, Date


stations_df = pd.read_csv('clean_stations.csv')
measurements_df = pd.read_csv('clean_measure.csv')
engine = create_engine('sqlite:///hawaii.sqlite')


metadata = MetaData()

stations = Table(
    'stations', metadata,
    Column('station', String, primary_key=True),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('elevation', Float),
    Column('name', String),
    Column('country', String),
    Column('state', String)
)


measurements = Table(
    'measurements', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('station', String),
    Column('date', Date),
    Column('precip', Float),
    Column('tobs', Integer)
)

metadata.create_all(engine)

stations_df.to_sql('stations', con=engine, if_exists='append', index=False)

measurements_df.to_sql('measurements', con=engine, if_exists='append', index=False)

with engine.connect() as conn:
    result = conn.execute("SELECT * FROM stations LIMIT 5").fetchall()
    print(result)