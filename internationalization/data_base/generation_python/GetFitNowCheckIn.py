from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from Base import Base, Session, engine

import random
import GetFitNowMembers

Base.metadata.create_all(engine)
session = Session()

class GetFitNowCheckIn(Base):
    __abstract__ = True
    #__tablename__ = 'get_fit_now_check_ins'
    check_in_date = Column('check_in_date', Integer, primary_key=True)
    check_in_time = Column('check_in_time', Integer, primary_key=True)
    check_out_time = Column('check_out_time', Integer, primary_key=True)

    def __init__(self, check_in_date, check_in_time, check_out_time):
        self.check_in_date = check_in_date
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time

    """ Randomly attributes a date for the check_in between start_year and end_year
        Attributes : start_year, end_year (integers) """

    def set_check_in_date(self, start_year, end_year):
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

        self.check_in_date = int(c)

    """ Randomly attributes a check-in and a check-out time """

    def set_check_times(self):
        # random check-in time
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)
        self.check_in_time = str(hour) + str(minute)

        # random check-out time
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)
        self.check_out_time = str(hour) + str(minute)

class GetFitNowCheckInFrench(GetFitNowCheckIn):
    __tablename__ = 'visites_que_du_muscle'
    id_membre = Column(Text, ForeignKey('membres_que_du_muscle.id'))
    membership = relationship("GetFitNowMemberFrench")

    def __init__(self, membership):
        GetFitNowCheckIn.__init__(self, self.check_in_date, self.check_in_time, self.check_out_time)
        self.set_check_in_date(2017, 2019)
        self.set_check_times()

        self.membership = membership

