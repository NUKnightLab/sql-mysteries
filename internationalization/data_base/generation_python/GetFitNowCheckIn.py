from sqlalchemy import Column, Integer, Text, ForeignKey

from sqlalchemy.orm import relationship

from .Base import Base


class GetFitNowCheckIn(Base):

    def __init__(self):
        __tablename__ = 'get_fit_now_check_ins'
        membership_id = Column('membership_id', Text, ForeignKey('get_fit_now_members.id'))
        membership = relationship("GetFitNowCheckInMember", backref="get_fit_neow_check_ins")
        check_in_date = Column('check_in_date', Integer)
        check_in_time = Column('check_in_time', Integer)
        check_out_time = Column('check_out_time', Integer)


class GetFitNowCheckInFrench(GetFitNowCheckIn):
    def __init__(self):
        GetFitNowCheckIn.__init__(self)
        self.__tablename__ = 'visites_que_du_muscle'
        self.membership_id = Column('id_membre', Text, ForeignKey('membres_que_du_muscle.id'))
        self.membership = relationship("GetFitNowMemberFrench", backref="visites_que_du_muscle")
        self.check_in_date = Column('date_entree', Integer)
        self.check_in_time = Column('heure_entree', Integer)
        self.check_out_time = Column('heure_sortie', Integer)

# TODO: fill the table (abstract methods in the english class, french method in the french class
