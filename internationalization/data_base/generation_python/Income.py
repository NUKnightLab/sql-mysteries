from sqlalchemy import Column, Integer

from .Base import Base


class Income(Base):

    def __init__(self):
        __tablename__ = 'incomes'
        ssn = Column('ssn', Integer, primary_key=True, sqlite_autoincrement=True)
        annual_income = Column('annual_income', Integer)


class IncomeFrench(Income):
    def __init__(self):
        Income.__init__(self)
        self.__tablename__ = 'revenus'
        self.ssn = Column('nir', Integer)
        self.annual_income = Column('revenus_annuel', Integer)

# TODO: fill the table (abstract methods in the english class, french method in the french class
