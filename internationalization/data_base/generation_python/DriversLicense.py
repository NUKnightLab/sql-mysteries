from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from Base import Base, Session, engine

import random
import string

Base.metadata.create_all(engine)
session = Session()


class DriversLicense(Base):
    __abstract__ = True
    #__tablename__ = 'drivers_licenses'
    id = Column(Integer, primary_key=True)
    age = Column('age', Integer)
    height = Column('height', Integer)
    eye_color = Column('eye_color', Text)
    hair_color = Column('hair_color', Text)
    gender = Column('gender', Text)
    plate_number = Column('plate_number', Text)
    car_make = Column('car_make', Text)
    car_model = Column('car_model', Text)

    def __init__(self, age, height, eye_color, hair_color, gender, plate_number, car_make, car_model):
        self.age = age
        self.height = height
        self.eye_color = eye_color
        self.hair_color = hair_color
        self.gender = gender
        self.plate_number = plate_number
        self.car_make = car_make
        self.car_model = car_model

    """ Randomly fills in the age of the driver
        Arguments : age_min, age_max (integers) """
    def set_age(self, age_min, age_max):
        self.age = random.randint(age_min, age_max)

    """ Randomly fills in the height of the driver
            Arguments : h_min, h_max (integers) """
    def set_height(self, h_min, h_max):
        self.height = random.randint(h_min, h_max)

    """ Randomly fills in the eye color
        Argument : eye_colors(list) """
    def set_eye_color(self, eye_colors):
        self.eye_color = random.choice(eye_colors)

    """ Randomly fills in the hair color
        Argument : hair_colors(list) """
    def set_hair_color(self, hair_colors):
        self.hair_color = random.choice(hair_colors)

    """ Randomly fills in the gender of the driver
        Argument : genders(list) """
    def set_gender(self, genders):
        self.gender = random.choice(genders)

    """ Randomly fills in the car makers
        Argument : car_makers(path_file) : path to the file with the list of car makers you want to feature (one maker 
        per line, and in a readable format) """
    def set_car_make(self, car_makers):
        file = open(car_makers, "r")
        # get the number of lines in the file
        n = 0
        line = file.readline()
        while line:
            n += 1
            line = file.readline()
        file.close()
        # get a random line to pick the car maker
        index = random.randint(0, n-1)
        file = open(car_makers, "r")
        car_maker = file.readline()
        count = 0
        while count < index:
            count += 1
            car_maker = file.readline()
        self.car_make = car_maker

    """ Randomly fills in the car model
        Argument : car_models(path_file) : path to the file with the list of car models you want to feature (one model 
        per line, and in a readable format) """
    def set_car_model(self, car_models):
        file = open(car_models, "r")
        # get the number of lines in the file
        n = 0
        line = file.readline()
        while line:
            n += 1
            line = file.readline()
        file.close()
        # get a random line to pick the car model
        index = random.randint(0, n-1)
        file = open(car_models, "r")
        car_model = file.readline()
        count = 0
        while count < index:
            count += 1
            car_model = file.readline()
        self.car_model = car_model


class DriversLicenseFrench(DriversLicense):
    __tablename__ = 'permis_de_conduire'

    def set_plate_number(self):
        # making of plaque_number following French standards
        l1 = random.choice(string.ascii_uppercase)
        l2 = random.choice(string.ascii_uppercase)
        m = random.randint(100, 999)
        l3 = random.choice(string.ascii_uppercase)
        l4 = random.choice(string.ascii_uppercase)

        self.plate_number = l1 + l2 + "-" + str(m) + "-" + l3 + l4

    def __init__(self):
        eye_colors = ["noisette", "noir", "bleu", "marron", "vert"]
        hair_colors = ["noir", "blond", "chatain", "gris", "blanc", "roux"]
        genders = ["féminin", "masculin"]

        DriversLicense.__init__(self, self.age, self.height, self.eye_color, self.hair_color, self.gender,
                                self.plate_number, self.car_make, self.car_model)
        self.set_age(18, 90)
        self.set_height(150, 200)
        self.set_eye_color(eye_colors)
        self.set_hair_color(hair_colors)
        self.set_gender(genders)
        self.set_plate_number()
        self.set_car_make("../model_txt/makers_list.txt")
        self.set_car_model("../model_txt/models_list.txt")

