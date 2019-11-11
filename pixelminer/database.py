from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey

Base = declarative_base()


class BaseModel(Base):
    """A Base model for all PixelMiner models."""

    __abstract__ = True


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return Column(
        ForeignKey(f'{tablename}.{pk_name}'),
        nullable=nullable, **kwargs)


def initialize_engine(configuration):
    engine = create_engine(configuration['DATABASE']['URI'])
    return engine
