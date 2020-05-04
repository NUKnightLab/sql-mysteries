# -*- coding: utf-8 -*-

import sqlite3


def create():
    # database creation under the name sql-murder-mystery-francais.db

    # connexion to the database, and if necessary creation of it
    connexion = sqlite3.connect("sql-murder-mystery-francais.db")

    # getting a cursor
    cursor = connexion.cursor()

    # foreign keys activation
    cursor.execute("PRAGMA foreign_keys = ON")

    # table creation
    # drivers_license table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS permis_conduire(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        age INTEGER,
        taille INTEGER,
        couleur_yeux TEXT,
        couleur_cheveux TEXT,
        sexe TEXT,
        numero_plaque TEXT,
        marque_voiture TEXT,
        modele_voiture TEXT
    )''')

    # person table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS personnes(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        nom TEXT,
        id_permis INTEGER NOT NULL,
        numero_adresse INTEGER, 
        rue_adresse TEXT,
        nir INTEGER,
        FOREIGN KEY(id_permis) REFERENCES permis_conduire(id)
        ON DELETE CASCADE)
    ''')

    # interview table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS interrogatoires(
        id_personne INTEGER,
        compte_rendu TEXT,
        FOREIGN KEY(id_personne) REFERENCES personnes(id)
        ON DELETE CASCADE)
    ''')

    # facebook_event_checkin table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS entree_evenement_facebook(
        id_personne INTEGER,
        id_evenement INTEGER,
        nom_evenement TEXT,
        date INTEGER,
        FOREIGN KEY(id_personne) REFERENCES personnes(id)
        ON DELETE CASCADE)
    ''')

    # get_fit_now_member table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS membres_que_du_muscle(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        id_personne INTEGER,
        nom TEXT,
        debut_adhesion INTEGER,
        statut_adhesion INTEGER,
        FOREIGN KEY(id_personne) REFERENCES personnes(id)
        ON DELETE CASCADE)
    ''')

    # get_fit_now_check_in table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS visites_que_du_muscle(
        id_membre TEXT,
        date_entree INTEGER,
        heure_entree  TEXT,
        heure_sortie TEXT, 
        FOREIGN KEY(id_membre) REFERENCES membres_que_du_muscle(id)
        ON DELETE CASCADE)
    ''')

    # crime_scene_report table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS rapport_scene_crime(
        date INTEGER,
        categorie TEXT,
        description TEXT,
        ville TEXT
    )''')

    # income table translated
    cursor.execute('''CREATE TABLE IF NOT EXISTS revenus(
        nir INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        revenu_annuel INTEGER
    )''')

    # solution table translated
    cursor.execute(''' CREATE TABLE IF NOT EXISTS solution(
        user INTEGER,
        value TEXT
    )''')

    # commit of the modifications done to the table
    connexion.commit()

    # database disconnection
    connexion.close()
