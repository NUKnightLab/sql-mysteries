# -*- coding: utf-8 -*-

# inserts the clues leading to the solution into the table

import sqlite3
import random


def fill_clues(nb_entries):
    connexion = sqlite3.connect("../sql-murder-mystery-french.db")
    cursor = connexion.cursor()

    # create the report
    type_of_crime = "meurtre"
    date = 20190504
    description = "Les caméras de surveillance montrent 2 témoins sur la scène du crime. Le premier habite la " \
                  "dernière maison de 'GENERAL DE GAULLE (Avenue du)'. Le deuxième témoin, nommée ROXANE, habite " \
                  "quelque part sur 'GAMBETTA (Boulevard)'."
    city = "SQL Ville"

    data = [date, type_of_crime, description, city]
    cursor.execute('''INSERT INTO rapports_scene_de_crime(date, type, description, city) VALUES (?, ?, ?, ?)''', data)

    # create the two witnesses
    id_witness_1 = random.randint(0, nb_entries)
    name = 'MARIUS DUBOIS'
    address_number = 999
    address_street_name = 'GENERAL DE GAULLE (Avenue du)'
    ssn = 17406150424
    data = (name, address_number, address_street_name, ssn, id_witness_1)
    cursor.execute('''UPDATE personnes SET name = ?, address_number = ?, address_street_name = ?, ssn = ? WHERE 
    id = ? ''', data)

    id_witness_2 = random.randint(0, nb_entries)
    for id_witness_2 in [id_witness_1]:
        id_witness_2 = random.randint(0, nb_entries)
    name = 'ROXANE FAURE'
    address_number = random.randint(1, 999)
    address_street_name = 'GAMBETTA (Boulevard)'
    ssn = '08406156524'
    data = (name, address_number, address_street_name, ssn, id_witness_2)
    cursor.execute('''UPDATE personnes SET name = ?, address_number = ?, address_street_name = ?, ssn = ? WHERE 
        id = ? ''', data)

    # create the interviews for the two witnesses
    transcript_1 = "J'ai entendu un coup de feu et j'ai vu un homme sortir en courant. Il avait un sac de sport 'Que " \
                   "du muscle'.. Je sais que seulement les membres 'or' ont ce sac. L'homme est ensuite monté dans une"\
                   " voiture avec la plate qui comprennait l'inscription 'LTD'"
    data = (transcript_1, id_witness_1)
    cursor.execute('''UPDATE temoignages SET transcript = ? WHERE person_id = ? ''', data)

    transcript_2 = "J'ai vu le meurtre se dérouler, et j'ai reconnu le meurtrier : je l'ai vu au club de gym la " \
                   "semaine dernière, le 25 avril"
    data = (transcript_2, id_witness_2)
    cursor.execute('''UPDATE temoignages SET transcript = ? WHERE person_id = ? ''', data)

    # create the member of the gym club (the suspect)
    # in get_fit_now_checkin
    id_suspect = random.randint(0, nb_entries)
    for id_suspect in [id_witness_1, id_witness_2]:
        id_suspect = random.randint(0, nb_entries)
    date = '20190425'
    data = (date, id_suspect)
    cursor.execute('''UPDATE visites_que_du_muscle SET check_in_date = ? WHERE id_membre = ? ''', data)

    # in get_fit_now_member
    status = 'or'
    data = (status, id_suspect)
    cursor.execute('''UPDATE membres_que_du_muscle SET membership_status = ? WHERE id_personne = ? ''', data)

    # in drivers_license
    plate_number = 'LTD-619-DM'
    gender = 'masculin'
    data = (plate_number, gender, id_suspect)
    cursor.execute('''UPDATE permis_de_conduire SET plate_number = ?, gender = ? WHERE id = ? ''', data)

    # transcript of the suspect's interview
    transcript_suspect = "J'ai été engagé par une femme. Je ne sais pas comment elle s'apelle, mais je sais qu'elle " \
                         "fait 165 ou 170 cm. Elle a les cheveux roux et conduit une Tesla Model S. Je sais aussi " \
                         "qu'elle est allée au Concert Philarmonique de SQL Ville 3 fois en Décembre 2017."

    data = (transcript_suspect, id_suspect)
    cursor.execute('''UPDATE temoignages SET transcript = ? WHERE person_id = ? ''', data)

    # the partner's drivers license
    id_partner = random.randint(0, nb_entries)
    for id_partner in [id_witness_1, id_witness_2, id_suspect]:
        id_partner = random.randint(0, nb_entries)
    gender = 'féminin'
    height = 165
    hair_color = 'roux'
    car_make = 'Tesla'
    car_model = 'Model S'

    data = (gender, height, hair_color, car_make, car_model, id_partner)
    cursor.execute('''UPDATE permis_de_conduire SET gender = ?, height = ?, hair_color = ?, car_make = ?, car_model = ?
     WHERE id = ? ''', data)

    # facebook event check_in
    event_name = 'Concert Philarmonique de SQL Ville'
    event_ids = []
    for i in range(3):
        day = random.randint(1, 31)
        date = '201712'+str(day)
        event_id = random.randint(0, nb_entries)
        for j in [event_ids]:
            event_id = random.randint(0, nb_entries)
        event_ids += [event_id]
    data = (event_name, id_partner, date, event_id)
    cursor.execute('''UPDATE Evenement_Facebook SET event_name = ?, person_id = ?, date = ? WHERE event_id = ? ''', data)

    # person entry for the partner
    partner_name = 'IRENE ADLER'
    data = [partner_name, id_partner]
    cursor.execute('''UPDATE personnes SET name = ? WHERE id = ?''', data)

    connexion.commit()
    connexion.close()
