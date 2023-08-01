from Base import Base, Session, engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, ForeignKey

import random
import string

Base.metadata.create_all(engine)
session = Session()


class Person(Base):
    __abstract__ = True
    #__tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column('name', Text)
    address_number = Column('address_number', Integer)
    address_street_name = Column('address_street_name', Text)
    ssn = Column('ssn', Text)

    def __init__(self, name, address_number, address_street_name, ssn):
        self.name = name
        self.address_number = address_number
        self.address_street_name = address_street_name
        self.ssn = ssn

    """ Randomly fills in the name
        Argument : firstNames(path_file) : path to the file with the list of names you want to feature (one name
        per line, and in a readable format), same for lastNames"""
    def set_name(self, firstnames, lastnames):
        # get the number of lines in the first file
        firstname_file = open(firstnames, "r")
        n_firstname = 0
        line = firstname_file.readline()
        while line:
            n_firstname += 1
            line = firstname_file.readline()
        firstname_file.close()

        # get the number of lines in the first file
        lastname_file = open(lastnames, "r")
        n_lastname = 0
        line = lastname_file.readline()
        while line:
            n_lastname += 1
            line = lastname_file.readline()
        lastname_file.close()

        # get a random line to pick the names
        index_first = random.randint(0, n_firstname - 1)
        index_last = random.randint(0, n_lastname - 1)
        firstname_file = open(firstnames, "r")
        lastname_file = open(lastnames, "r")
        firstname = firstname_file.readline()
        lastname = lastname_file.readline()
        count = 0

        while count < index_first:
            count += 1
            firstname = firstname_file.readline()

        while count < index_last:
                count += 1
                lastname = lastname_file.readline()

        self.name = firstname + " " + lastname

    """ Randomly attributes a number for the adress_number between 1 and 999 """
    def set_adresse_number(self):
        self.address_number = random.randint(1, 999)

    """ Randomly fills in the name
       Argument : street_name(path_file) : path to the file with the list of names you want to feature (one name
       per line, and in a readable format) """
    def set_address_street_name(self, path_file):
        # get the number of lines in the file
        file = open(path_file, "r")
        n = 0
        line = file.readline()
        while line:
            n += 1
            line = file.readline()
        file.close()

        index = random.randint(1, n)
        file = open(path_file, "r")
        street_name = file.readline()
        count = 0
        while count < index:
            count += 1
            street_name = file.readline()
        file.close()

        self.address_street_name = street_name

    """ Randomly generates a ssn following the French standards : 
        1st number : sex (0 for a man, 1 for a woman)
        2nd and 3rd number : last two numbers of the birth year
        4th and 5th : birth month
        6th and 7th : department code in which the person is born
        8th to 13th : random numbers"""
    def set_ssn(self):
        sex = random.randint(0, 1)

        birth_year = random.randint(0, 99)
        if birth_year < 10:
            birth_year = "0" + str(birth_year)

        birth_month = random.randint(1, 12)
        if birth_month < 10:
            birth_month = "0" + str(birth_month)

        birth_place = random.randint(100, 999)
        random_number = random.randint(100, 999)

        string_ssn = str(sex) + str(birth_year) + str(birth_month) + str(birth_place) + str(random_number)
        self.ssn = string_ssn

class PersonFrench(Person):
    __tablename__ = 'personnes'

    id_permis_de_conduire = Column(Integer, ForeignKey('permis_de_conduire.id'))
    license = relationship("DriversLicenseFrench")

    def __init__(self, license):
        Person.__init__(self, self.name, self.address_number, self.address_street_name, self.ssn)
        self.set_name("../model_txt/firstname_list.txt", "../model_txt/lastname_list.txt")
        self.set_adresse_number()
        self.set_address_street_name("../model_txt/streetnames_list.txt")
        self.set_ssn()

        self.license = license


