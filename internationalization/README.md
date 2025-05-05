SQL Murder Mystery in French
================================================================================

Authors : Adrien Triquet et Carla Danti, based on Knightlab's educational game : SQL Murder Mystery : https://mystery.knightlab.com/
--------------------------------------------------------------------------------

We are implementing a way to generate the database used in the game in French. It is coded as such as, if someone wants to implement their own translated version, they will have the pre existing structure to rely on.
--------------------------------------------------------------------------------

# data_base
The purpose is to generate a database in another language. For now, it is generating a french database. All the files  are to be executed with Pyhton 3, as well as SQL Lite (a library used to implement SQL databases).

## How to create the database
Execute generation-python/__main.py__, the database will be created in data-base. You need to open it with a database manager (advice : open it with SQLiteStudio).
It appeals to each files for each class. There is a mother and a child class for each table.

### main.py explanation
The begining of the code is simply to work with the ORM, as it needs an engine to modify the database. Then, tables are constructed when the classes are called, and added to the database.

## data_base directory description :
- **generation_python** : all the files with the code, each file being an obect class, except for Base.py which is necessary to use the ORM, and main.py which is the file to execute to generate the database. See a simple class like ‘interview’, which is more commented, to understand how it works.

- **model_txt** : all the files needed to gather information for the database, that is to say the file we usein the code to translate some information (car makers we want to feature, car models, cities, ...)

- two png schemas for the databases, **schema_english.png** the official database schema given by Kinghtlab for the game, and **schema_french.png**, the french schema we made our code on.

## Principle of the code
We use the ORM (Object-Relational Mapping) SQLAlchemy for SQLite with Python to build the database.

All python class are linked. They generate the database table they have the name of. The first class is any given file is the parent class, with the table attributes, the relations between the tables, and some functions to fill in the tables.
The second class of the file is the child class, used to generate the french database. Some functions are redefined, as the attribute they build can be sepcific to French language or culture (for example the car plate number conventions are specific to different parts of the world).
In addition, they have the heritages to make them work with the ORM.

### model_txt
All files in this directory are used to fill in the databse.
“cities_list.txt” is a list of the 277 biggest French towns, based on a Wikipedia list.
“makers_list.txt” is a list of the 60 car brands most used in France.
“noise_text.txt” is the text of a novel : “Le mystère de la chambre jaune” by Gaston Leroux. It is provided by the Project Gutenberg and is free to use. We use this text to fill the crime descriptions in the table crime_scene_report.
"firstname_list.txt" is a list of the most commun firstnames in France based on a small part of a government free access database.
"lastname_list.txt" is a list of the most commun lastnames in France based on a small part of a government free access database.
"streetname_list.txt" is a list  of name of streets in the city of Saint-Nazaire taken in part from https://sql.sh/2716-base-donnnees-rues-france according to their content policy.

--------------------------------------------------------------------------------

# translation_html
The purpose is to enable anyone without html skills to translate in is language.
We use gettext to generate a new html file with string of characters translated from the « walkthrough.html » file.
You can help translating in your language all the string of characters, they all are in « base.po ».
To generate the html, open « config », install python3 if needed. Then install packages needed and create .po and .mo following the instruction.
Then, in « translation.py », please modify all the « fr » according to your language.
Finally run the file. A « fr.hmtl » file is generated in « translation_html ».
You have to translate sentence after sentence. Unfortunately, some sentences are cut for gettext to work properly.
--------------------------------------------------------------------------------

### Licence :
Our work is under MIT License, based on Knightlab's educational game : SQL Murder Mystery


### Authors :
Carla Danti
Adrien Triquet
Both are Telecom SudParis students under the tutorship of Olivier Berger
