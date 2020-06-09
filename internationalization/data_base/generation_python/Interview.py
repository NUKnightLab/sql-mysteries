from sqlalchemy.sql.ddl import CreateSequence, DDL

from Base import Base, Session, engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, event
import random

Base.metadata.create_all(engine)

session = Session()

class Interview(Base):
    #abstract enable us to choose a tablename in our own language in the child class
    __abstract__ = True

    """ the name if therefor not needed, however you can comment the '__abstract__ = True' to choose the tablename
        direclty from the parent database """
    #__tablename__ = 'interviews'

    """ you need to change the names of the columns here for them to appear in your language
        id is automaticly filed by the ORM as a primary key """
    id = Column('id', Integer, primary_key=True)
    transcript = Column('transcript', Text)

    def __init__(self, transcript):
        self.transcript = transcript

    """ Randomly attributes a transcript to the report
        Arguments : path_file(char) : relative path leading to the file you want to use to set descriptions, must be in a 
        readable format
        start(int) : number of the line where you want to begin picking up lines for description
        end(int) : umber of the line where you want to end picking up the lines """""
    def set_transcript(self, path_file, start, end):
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
        transcript = file.readline()
        count = 0
        while count < index:
            count += 1
            transcript = file.readline()
        file.close()

        self.transcript = transcript

#Child Class who heritates from interview, please create your own in your language
class InterviewFrench(Interview):
    #tablename who is going to appear
    __tablename__ = 'temoignages'

    #Relationship with the class PersonFrench for the appearing column "person_id"
    person_id = Column(Integer, ForeignKey('personnes.id'))
    person = relationship("PersonFrench")

    #init of the class, when you call it, you need to give as a parameter a person of class Person
    def __init__(self, person):
        #the initialisation is made with parameters of the parent class
        Interview.__init__(self, self.transcript)
        self.person = person
        self.set_transcript("../model_txt/noise_text.txt", 77, 369)
