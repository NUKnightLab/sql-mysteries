from sqlalchemy import Column, Integer, Text, ForeignKey

from sqlalchemy.orm import relationship

from .Base import Base


class FacebookEventCheckIn(Base):

    def __init__(self):
        __tablename__ = 'facebook_events_checkins'
        person_id = Column(Integer, ForeignKey('person.id'))
        person = relationship("Person", backref="facebook_events_checkins")
        event_id = Column('event_id', Integer)
        event_name = Column('event_name', Text)
        date = Column('date', Integer)


class FacebookEventCheckInFrench(FacebookEventCheckIn):
    def __init__(self):
        FacebookEventCheckIn.__init__(self)
        self.__tablename__ = 'entrees_evenements_facebook'
        self.person_id = Column('id_personne', Integer, ForeignKey('personnes.id'))
        self.personne = relationship("PersonFrench", backref="entrees_evenements_facebook")
        self.event_id = Column('id_evenement', Integer)
        self.event_name = Column('nom_evenement', Text)

# TODO: fill the table (abstract methods in the english class, french method in the french class
