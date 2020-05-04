# -*- coding: utf-8 -*-

import os
import create
import fill


if os.path.exists("sql-murder-mystery-francais.db"):
    os.remove("sql-murder-mystery-francais.db")


create.create()
fill.fill_crime_scene_report()
fill.fill_drivers_license()
fill.fill_gfn_checkin()

# TODO : fill the tables with the clues leading to the solution
