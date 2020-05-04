# -*- coding: utf-8 -*-

import sqlite3
import string
import random


def fill_crime_scene_report():
    connexion = sqlite3.connect("sql-murder-mystery-francais.db")
    cursor = connexion.cursor()

    categories = ["incendie criminel", "agression", "chantage", "corruption", "fraude", "meurtre", "braquage",
                  "contrebande", "vol"]

    # get the number of lines in cities_list.txt
    file = open("../model_txt/cities_list.txt", "r")
    n_cities = 0
    line = file.readline()
    while line:
        n_cities += 1
        line = file.readline()
    file.close()

    # get the number of lines in the text to drown the clue in noise
    file = open("../model_txt/noise_text.txt", "r")
    n_lines = 0
    line = file.readline()
    while line:
        n_lines += 1
        line = file.readline()
    file.close()

    for i in range(999):
        # random attribution of crimes
        index = random.randint(0, 8)
        category = categories[index]

        # random date
        year = random.randint(2017, 2019)
        month = random.randint(1, 12)

        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        if month == 2:
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 30)

        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        c = str(year) + str(month) + str(day)
        date = int(c)

        # random city
        index = random.randint(1, n_cities)

        file = open("../model_txt/cities_list.txt", "r")
        city = file.readline()
        count = 0
        while count < index:
            count += 1
            city = file.readline()
        file.close()

        # random crime description
        # we begin at line 77 as the lines above it are descriptions and sources of the files, and 369 lines before
        # the end of file for the same reasons
        index = random.randint(77, n_lines-369)

        file = open("../model_txt/noise_text.txt", "r")
        description = file.readline()
        count = 0
        while count < index:
            count += 1
            description = file.readline()
        file.close()

        data = [category, date, description, city]

        cursor.execute(
            '''INSERT INTO rapport_scene_crime(categorie, date, description, ville) VALUES (?, ?, ?, ?)''', data
        )

    connexion.commit()
    connexion.close()


def fill_drivers_license():
    connexion = sqlite3.connect("sql-murder-mystery-francais.db")
    cursor = connexion.cursor()

    eyes_colors = ["noisette", "noir", "bleu", "marron", "vert"]
    hair_colors = ["noir", "blond", "chatain", "gris", "blanc", "roux"]
    sexes = ["féminin", "masculin"]

    file = open("../model_txt/makers_list.txt", "r")

    # get the number of lines in makers_list.txt
    n = 0
    line = file.readline()
    while line:
        n += 1
        line = file.readline()
    file.close()

    for i in range(999):
        age = random.randint(18, 90)
        height = random.randint(150, 200)
        eyes_color = random.choice(eyes_colors)
        hair_color = random.choice(hair_colors)
        sex = random.choice(sexes)

        # making of plaque_number following French standards
        l1 = random.choice(string.ascii_uppercase)
        l2 = random.choice(string.ascii_uppercase)
        m = random.randint(000, 999)
        l3 = random.choice(string.ascii_uppercase)
        l4 = random.choice(string.ascii_uppercase)

        plaque_number = l1 + l2 + "-" + str(m) + "-" + l3 + l4

        # random attribution of plaque numbers
        index = random.randint(0, n)

        file = open("../model_txt/makers_list.txt", "r")
        maker = file.readline()
        count = 0
        while count < index:
            count += 1
            maker = file.readline()
        data = [age, height, eyes_color, hair_color, sex, plaque_number, maker]
        cursor.execute(
            ''' INSERT INTO permis_conduire(age, taille, couleur_yeux, couleur_cheveux, sexe, numero_plaque, 
            marque_voiture) VALUES (?, ?, ?, ?, ?, ?, ?)''', data
        )
    connexion.commit()
    connexion.close()
    # TODO : random attribution of the car's model


def fill_person():
    connexion = sqlite3.connect("sql-murder-mystery-francais.db")
    cursor = connexion.cursor()

    for i in range(999):
        n = random.randint(000, 100)
        address_number = n

        license_number = random.randint(10000, 100000)

        data = [name, license_number, address_number, address_street, ssn]
        cursor.execute(''' INSERT INTO personnes(nom, id_permis, numero_adresse, rue_adresse, nir) VALUES
        (?, ?, ?, ?, ?) ''', data)

    connexion.commit()
    connexion.close()

    # TODO : fill in with random names, street names and ssn


def fill_gfn_checkin():
    connexion = sqlite3.connect("sql-murder-mystery-francais.db")
    cursor = connexion.cursor()

    for i in range(999):

        # random date
        year = random.randint(2017, 2019)
        month = random.randint(1, 12)

        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        if month == 2:
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 30)
        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        d = str(year) + str(month) + str(day)
        date = int(d)

        # random check-in time
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)
        checkin_time = str(hour) + str(minute)

        # random check-out hour
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)
        checkout_time = str(hour) + str(minute)

        data = [date, checkin_time, checkout_time]
        cursor.execute('''INSERT INTO visites_que_du_muscle(date_entree, heure_entree, heure_sortie) VALUES (?, ?, ?)'''
                       , data)

    connexion.commit()
    connexion.close()

# TODO : fill-in interviews, facebook_event_checkin, get-fit-now-members, income, solutions)
