from Base import Base, Session, engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, ForeignKey

import random

Base.metadata.create_all(engine)
session = Session()


class FacebookEventCheckIn(Base):
    __abstract__ = True
    #__tablename__ = 'facebook_events_checkins'
    event_id = Column('event_id', Integer, primary_key=True, autoincrement=True)
    event_name = Column('event_name', Text)
    date = Column('date', Integer)

    def __init__(self, event_name, date):
        self.event_name = event_name
        self.date = date

    """ Randomly attributes an event_name to the report
        Arguments : path_file(char) : relative path leading to the file you want to use to set descriptions, must be in 
        a readable format
        start(int) : number of the line where you want to begin picking up lines for description
        end(int) : umber of the line where you want to end picking up the lines """""

    def set_event_name(self, path_file, start, end):
        # get the number of lines in the text to hide the clues in the text
        file = open(path_file, "r")
        n_lines = 0
        line = file.readline()
        while line:
            n_lines += 1
            line = file.readline()
        file.close()

        index = random.randint(start, n_lines - end)

        file = open(path_file, "r")
        event_name = file.readline()
        count = 0
        while count < index:
            count += 1
            event_name = file.readline()
        file.close()

        self.event_name = event_name

    """ Randomly attributes a date between start_year and end_year
      Attributes : start_year, end_year (integers) """
    def set_date(self, start_year, end_year):
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

        self.date = int(c)


class FacebookEventCheckInFrench(FacebookEventCheckIn):
    __tablename__ = 'Evenement_Facebook'

    person_id = Column(Integer, ForeignKey('personnes.id'))
    person = relationship("PersonFrench")

    def __init__(self, person):
        FacebookEventCheckIn.__init__(self, self.event_name, self.date)
        self.person = person
        self.set_event_name("../model_txt/noise_text.txt", 77, 369)
        self.set_date(2017, 2019)
