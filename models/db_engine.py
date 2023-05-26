import os
import sqlalchemy as sa

CONNECTION_STRING='postgresql+psycopg2://ggarcia:@localhost/friendface'
engine=sa.create_engine(CONNECTION_STRING, echo=True)
metadata = sa.MetaData()
metadata.create_all(engine)
