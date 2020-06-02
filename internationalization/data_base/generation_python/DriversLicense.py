from sqlalchemy import Column, Integer, Text

from .Base import Base


class DriversLicense(Base):

    def __init__(self):
        __tablename__ = 'drivers_licenses'
        id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
        age = Column('age', Integer)
        height = Column('height', Integer)
        eye_color = Column('eye_color', Text)
        hair_color = Column('hair_color', Text)
        gender = Column('gender', Text)
        plate_number = Column('plate_number', Text)
        car_make = Column('car_make', Text)
        car_model = Column('car_model', Text)


class DriversLicenseFrench(DriversLicense):
    def __init__(self):
        DriversLicense.__init__(self)
        self.__tablename__ = 'permis_conduire'
        self.height = Column('taille', Integer)
        self.eye_color = Column('couleur_yeux', Text)
        self.hair_color = Column('couleur_cheveux', Text)
        self.gender = Column('sexe', Text)
        self.plate_number = Column('numero_plaque', Text)
        self.car_make = Column('marque_voiture', Text)
        self.car_model = Column('modele_voiture', Text)

# TODO: fill the table (abstract methods in the english class, french method in the french class
