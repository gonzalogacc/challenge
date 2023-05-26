import sqlalchemy
import sqlalchemy as sa
from sqlalchemy import inspect

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from models.db_engine import engine

def as_dict(self):
    return {c.key: getattr(self, c.key) for c in
            inspect(self).mapper.column_attrs}

meta = sa.MetaData(naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_key",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey"
      })

Base = declarative_base(metadata=meta)
Base.as_dict = as_dict

class Files(Base):
    """ """
    __tablename__ = "files"

    id = sa.Column(sa.Integer, primary_key=True)

    uuid = sa.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    name = sa.Column(sa.String)
    media_type = sa.Column(sa.String)
    service = sa.Column(sa.String)

    tags = relationship("FileTags", back_populates="file")

    def __repr__(self):
        return f"<id={self.id}:{self.uuid}, name={self.name}>"

class Tags(Base):
    __tablename__ = "tags"

    id = sa.Column(sa.Integer, primary_key=True)

    uuid = sa.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    name = sa.Column(sa.String)
    
    files = relationship("FileTags", back_populates="tag")

    def __repr__(self):
        return f"<id={self.id}:{self.uuid}, name={self.name}>"
   
class FileTags(Base):
    __tablename__ = "file_tags"
    file_id = sa.Column(sa.Integer, sa.ForeignKey("files.id"), primary_key=True)
    tag_id = sa.Column(sa.Integer, sa.ForeignKey("tags.id"), primary_key=True)

    file = relationship("Files", back_populates="tags")
    tag = relationship("Tags", back_populates="files")

