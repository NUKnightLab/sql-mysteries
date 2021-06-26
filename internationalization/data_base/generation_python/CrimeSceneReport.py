from sqlalchemy import Column, Integer, Text
from Base import Base, Session, engine

import random

Base.metadata.create_all(engine)
session = Session()


class CrimeSceneReport(Base):
    __abstract__ = True
    __tablename__ = 'crime_scene_reports'
    #in order not to have an "id" column appearing in the database, we put all those columns as primary_keys
    date = Column(Integer, primary_key=True)
    type = Column(Text, primary_key=True)
    description = Column(Text, primary_key=True)
    city = Column(Text, primary_key=True)

    def __init__(self, type_of_crime, date, city, description):
        self.date = date
        self.type = type_of_crime
        self.description = description
        self.city = city

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

    """ Randomly attributes a description to the report
    Arguments : path_file(char) : relative path leading to the file you want to use to set descriptions, must be in a 
    readable format
    start(int) : number of the line where you want to begin picking up lines for description
    end(int) : umber of the line where you want to end picking up the lines """""

    def set_description(self, path_file, start, end):
        # get the number of lines in the text to drown the clue in noise
        file = open(path_file, "r")
        n_lines = 0
        line = file.readline()
        while line:
            n_lines += 1
            line = file.readline()
        file.close()

        index = random.randint(start, n_lines - end)

        file = open(path_file, "r")
        description = file.readline()
        count = 0
        while count < index:
            count += 1
            description = file.readline()
        file.close()

        self.description = description

    """ Randomly fills in the type of crime committed
    Argument : types(list) : list of the type of crimes you want to put in the database """
    def set_type(self, types):
        index = random.randint(0, len(types)-1)
        type_of_crime = types[index]

        self.type = type_of_crime

    """ Randomly selects a city on a given file (one city per line, and in a readable format)
    Arguments : path_file : relative path to the list of cities """
    def set_city(self, path_file):
        # get the number of lines in the file
        file = open(path_file, "r")
        n_cities = 0
        line = file.readline()
        while line:
            n_cities += 1
            line = file.readline()
        file.close()

        index = random.randint(1, n_cities)
        file = open(path_file, "r")
        city = file.readline()
        count = 0
        while count < index:
            count += 1
            city = file.readline()
        file.close()

        self.city = city


class CrimeSceneReportFrench(CrimeSceneReport):
    __tablename__ = 'rapports_scene_de_crime'

    def __init__(self):
        self.city = Column('ville', Text)

        types = ["incendie criminel", "agression", "chantage", "corruption", "fraude", "meurtre", "braquage",
                 "contrebande", "vol"]

        CrimeSceneReport.__init__(self, self.type, self.city, self.description, self.date)
        self.set_date(2017, 2019)
        self.set_description("../model_txt/noise_text.txt", 77, 369)
        self.set_type(types)
        self.set_city("../model_txt/cities_list.txt")
