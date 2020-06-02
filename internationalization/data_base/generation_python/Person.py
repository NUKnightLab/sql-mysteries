from sqlalchemy import Column, Integer, Text, ForeignKey

from sqlalchemy.orm import relationship, backref

from .Base import Base


class Person(Base):

    def __init__(self):
        __tablename__ = 'persons'
        id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
        name = Column('name', Text)
        license_id = Column(Integer, ForeignKey('drivers_licenses.id'))
        license = relationship("DriversLicense", backref=backref("person", uselist=False))
        address_number = Column('address_number', Integer)
        address_street_name = Column('address_street_name', Text)
        ssn = Column('ssn', Integer)


class PersonFrench(Person):
    def __init__(self):
        Person.__init__(self)
        self.__tablename__ = 'personnes'
        self.name = Column('nom', Text)
        self.license_id = Column('id_permis', Integer, ForeignKey('permis_conduire.id'))
        self.licence = relationship("DriversLicenseFrench", backref=backref("personne", uselist=False))
        self.address_number = Column('numero_adresse', Integer)
        self.address_street_name = Column('rue_adresse', Text)
        self.ssn = Column('nir', Integer)

# TODO: fill the table (abstract methods in the english class, french method in the french class
