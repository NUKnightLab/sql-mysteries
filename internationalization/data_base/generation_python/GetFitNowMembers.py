from sqlalchemy import Column, Integer, Text, ForeignKey

from sqlalchemy.orm import relationship, backref

from .Base import Base


class GetFitNowMember(Base):

    def __init__(self):
        __tablename__ = 'get_fit_now_members'
        id = Column(Text, primary_key=True, sqlite_autoincrement=True)
        person_id = Column(Integer, ForeignKey('persons.id'))
        person = relationship("Person", backref=backref("get_fit_now_membership", uselist=False))
        name = Column('name', Text)
        membership_start_date = Column('membership_start_date', Integer)
        membership_status = Column('membership_status', Text)


class GetFitNowMemberFrench(GetFitNowMember):
    def __init__(self):
        GetFitNowMember.__init__(self)
        self.__tablename__ = 'membres_que_du_muscle'
        self.person_id = Column('id_personne', Integer, ForeignKey('personnes.id'))
        self.person = relationship("PersonFrench", backref=backref("membre_que_du_muscle", uselist=False))
        self.name = Column('nom', Text)
        self.membership_start_date = Column('debut_adhesion', Integer)
        self.membership_status = Column('statut_adhesion', Integer)

# TODO: fill the table (abstract methods in the english class, french method in the french class
