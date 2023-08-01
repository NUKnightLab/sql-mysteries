# -*- coding: utf-8 -*-
import random

from Base import Session, engine, Base
import os

from sqlalchemy.orm import query

from CrimeSceneReport import CrimeSceneReportFrench
from DriversLicense import DriversLicenseFrench
from GetFitNowCheckIn import GetFitNowCheckInFrench
from Person import PersonFrench
from Interview import InterviewFrench
from FacebookEventCheckIn import FacebookEventCheckInFrench
from GetFitNowMembers import GetFitNowMemberFrench

import Solution

# check if the database has already been generated
if os.path.exists('data_base/sql-murder-mystery-french.db'):
    os.remove('data_base/sql-murder-mystery-french.db')

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()

# number of values in the table
nb = 999

# create entries to persist in the database
for i in range(nb):

    # create the tables in french
    crime_scene_report = CrimeSceneReportFrench()
    drivers_license = DriversLicenseFrench()
    person = PersonFrench(drivers_license)

    """ those following tables call a person as argument
        each get_fit_now_members or interview will then be generated with the person created in the same loop
        get_fit_now_members taked twice the same argument because it is needed for two columns """
    get_fit_now_members = GetFitNowMemberFrench(person, person)
    interview = InterviewFrench(person)

    # add the tables to the database
    session.add(crime_scene_report)
    session.add(drivers_license)
    session.add(person)
    session.add(get_fit_now_members)
    session.add(interview)


# Many to One : we make another loop because for them we need the rest of the database to be already filled
for i in range(nb):
    #we take a random member in the existing database
    rand1 = random.randrange(0, nb)
    get_fit_now_member = session.query(GetFitNowMemberFrench)[rand1]
    #we create a check_in for this member
    get_fit_now_check_in = GetFitNowCheckInFrench(get_fit_now_member)

    # we take a random person in the existing database
    rand2 = random.randrange(0, nb)
    person = session.query(PersonFrench)[rand2]
    # we create a check_in for this person
    facebook_event_check_in = FacebookEventCheckInFrench(person)

    # add the tables to the database
    session.add(facebook_event_check_in)
    session.add(get_fit_now_check_in)

# commit and close session
session.commit()
session.close()

# insert the clues
Solution.fill_clues(nb)
