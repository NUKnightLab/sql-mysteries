from sqlalchemy import Column, Integer, Text

from .Base import Base


class Solution(Base):

    def __init__(self):
        __tablename__ = 'solutions'
        user = Column('user', Integer)
        value = Column('value', Text)


# TODO: fill the table (abstract methods)
