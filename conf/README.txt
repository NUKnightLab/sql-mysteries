SQLiteデータベース解析結果
==================================================

テーブル: crime_scene_report
行数: 1228
列:
  - date (INTEGER)
  - type (TEXT)
  - description (TEXT)
  - city (TEXT)

テーブル: drivers_license
行数: 10007
列:
  - id (INTEGER)
  - age (INTEGER)
  - height (INTEGER)
  - eye_color (TEXT)
  - hair_color (TEXT)
  - gender (TEXT)
  - plate_number (TEXT)
  - car_make (TEXT)
  - car_model (TEXT)

テーブル: facebook_event_checkin
行数: 20011
列:
  - person_id (INTEGER)
  - event_id (INTEGER)
  - event_name (TEXT)
  - date (INTEGER)

テーブル: get_fit_now_check_in
行数: 2703
列:
  - membership_id (TEXT)
  - check_in_date (INTEGER)
  - check_in_time (INTEGER)
  - check_out_time (INTEGER)

テーブル: get_fit_now_member
行数: 184
列:
  - id (TEXT)
  - person_id (INTEGER)
  - name (TEXT)
  - membership_start_date (INTEGER)
  - membership_status (TEXT)

テーブル: income
行数: 7514
列:
  - ssn (CHAR)
  - annual_income (INTEGER)

テーブル: interview
行数: 4991
列:
  - person_id (INTEGER)
  - transcript (TEXT)

テーブル: person
行数: 10011
列:
  - id (INTEGER)
  - name (TEXT)
  - license_id (INTEGER)
  - address_number (INTEGER)
  - address_street_name (TEXT)
  - ssn (CHAR)

テーブル: solution
行数: 0
列:
  - user (INTEGER)
  - value (TEXT)

