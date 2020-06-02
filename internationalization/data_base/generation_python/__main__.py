# -*- coding: utf-8 -*-
from Base import Session, engine, Base
from CrimeSceneReport import CrimeSceneReportFrench

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()

# create entries to persist in the database
for i in range(999):

    # create crime scene reports in french
    crime_scene_report = CrimeSceneReportFrench()

    # add the reports to the database
    session.add(crime_scene_report)

# commit and close session
session.commit()
session.close()


# TODO : adapt the main file to the ORM use
# TODO : fill the tables with the clues leading to the solution
