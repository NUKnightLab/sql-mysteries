from sqlalchemy import Column, Integer, Text, ForeignKey

from sqlalchemy.orm import relationship

from .Base import Base


class Interview(Base):

    def __init__(self):
        __tablename__ = 'interviews'
        person_id = Column(Integer, ForeignKey('person.id'))
        person = relationship("Person", backref="interviews")
        transcript = Column('transcript', Text)


class InterviewFrench(Interview):
    def __init__(self):
        Interview.__init__(self)
        self.__tablename__ = 'interrogatoires'
        self.person_id = Column('id_personne', Integer, ForeignKey('personnes.id'))
        self.person = relationship("PersonFrench", backref="interrogatoires")
        self.transcript = Column('compte_rendu', Text)

# TODO: fill the table (abstract methods in the english class, french method in the french class
