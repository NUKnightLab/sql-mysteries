from Base import Base, Session, engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, ForeignKey

import random
import string
import Person

Base.metadata.create_all(engine)
session = Session()

class GetFitNowMember(Base):
    __abstract__ = True
    #__tablename__ = 'get_fit_now_members'
    id = Column('id', Integer, primary_key=True)
    membership_start_date = Column('membership_start_date', Integer)
    membership_status = Column('membership_status', Text)

    def __init__(self, membership_start_date, membership_status):
        self.membership_start_date = membership_start_date
        self.membership_status = membership_status

    """ Randomly attributes a date between start_year and end_year
         Attributes : start_year, end_year (integers) """
    def set_membership_start_date(self, start_year, end_year):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)

        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        if month == 2:
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 30)

        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        c = str(year) + str(month) + str(day)

        self.membership_start_date = int(c)

    """ Randomly fills in the status of the membership
        Argument : types(list) : list of the type of crimes you want to put in the database """
    def set_membership_status(self, types):
        index = random.randint(0, len(types) - 1)
        membership_status = types[index]

        self.membership_status = membership_status

class GetFitNowMemberFrench(GetFitNowMember):
    __tablename__ = 'membres_que_du_muscle'

    """ We need two 'person' to generate those two columns
        to have the id corresponding to the name, you need to call twice the same 'person' in 'main' """
    id_personne = Column(Integer, ForeignKey('personnes.id'))
    person1 = relationship("PersonFrench", foreign_keys=[id_personne])
    nom = Column(Text, ForeignKey('personnes.name'))
    person2 = relationship("PersonFrench", foreign_keys=[nom])

    def __init__(self, person1, person2):
        status = ["normal", "or", "argent"]

        GetFitNowMember.__init__(self, self.membership_start_date, self.membership_status)

        self.set_membership_start_date(2015, 2017)
        self.set_membership_status(status)

        self.person1 = person1
        self.person2 = person2