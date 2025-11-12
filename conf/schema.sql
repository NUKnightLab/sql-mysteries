-- Table: crime_scene_report
CREATE TABLE crime_scene_report (
        date integer,
        type text,
        description text,
        city text
    );

-- Columns for crime_scene_report:
--   date: INTEGER
--   type: TEXT
--   description: TEXT
--   city: TEXT

-- Table: drivers_license
CREATE TABLE drivers_license (
        id integer PRIMARY KEY,
        age integer,
        height integer,
        eye_color text,
        hair_color text,
        gender text,
        plate_number text,
        car_make text,
        car_model text
    );

-- Columns for drivers_license:
--   id: INTEGER (PRIMARY KEY)
--   age: INTEGER
--   height: INTEGER
--   eye_color: TEXT
--   hair_color: TEXT
--   gender: TEXT
--   plate_number: TEXT
--   car_make: TEXT
--   car_model: TEXT

-- Table: facebook_event_checkin
CREATE TABLE facebook_event_checkin (
        person_id integer,
        event_id integer,
        event_name text,
        date integer,
        FOREIGN KEY (person_id) REFERENCES person(id)
    );

-- Columns for facebook_event_checkin:
--   person_id: INTEGER
--   event_id: INTEGER
--   event_name: TEXT
--   date: INTEGER

-- Table: get_fit_now_check_in
CREATE TABLE get_fit_now_check_in (
        membership_id text,
        check_in_date integer,
        check_in_time integer,
        check_out_time integer,
        FOREIGN KEY (membership_id) REFERENCES get_fit_now_member(id)
    );

-- Columns for get_fit_now_check_in:
--   membership_id: TEXT
--   check_in_date: INTEGER
--   check_in_time: INTEGER
--   check_out_time: INTEGER

-- Table: get_fit_now_member
CREATE TABLE get_fit_now_member (
        id text PRIMARY KEY,
        person_id integer,
        name text,
        membership_start_date integer,
        membership_status text,
        FOREIGN KEY (person_id) REFERENCES person(id)
    );

-- Columns for get_fit_now_member:
--   id: TEXT (PRIMARY KEY)
--   person_id: INTEGER
--   name: TEXT
--   membership_start_date: INTEGER
--   membership_status: TEXT

-- Table: income
CREATE TABLE income (ssn CHAR PRIMARY KEY, annual_income integer);

-- Columns for income:
--   ssn: CHAR (PRIMARY KEY)
--   annual_income: INTEGER

-- Table: interview
CREATE TABLE interview (
        person_id integer,
        transcript text,
        FOREIGN KEY (person_id) REFERENCES person(id)
    );

-- Columns for interview:
--   person_id: INTEGER
--   transcript: TEXT

-- Table: person
CREATE TABLE person (id integer PRIMARY KEY, name text, license_id integer, address_number integer, address_street_name text, ssn CHAR REFERENCES income (ssn), FOREIGN KEY (license_id) REFERENCES drivers_license (id));

-- Columns for person:
--   id: INTEGER (PRIMARY KEY)
--   name: TEXT
--   license_id: INTEGER
--   address_number: INTEGER
--   address_street_name: TEXT
--   ssn: CHAR

-- Table: solution
CREATE TABLE solution (
        user integer,
        value text
    );

-- Columns for solution:
--   user: INTEGER
--   value: TEXT

