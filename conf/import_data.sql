-- CSVファイルからデータをインポートするスクリプト
-- 使用方法: sqlite3 new_database.db < import_data.sql

-- crime_scene_reportテーブル
.mode csv
.import crime_scene_report.csv crime_scene_report

-- drivers_licenseテーブル
.mode csv
.import drivers_license.csv drivers_license

-- facebook_event_checkinテーブル
.mode csv
.import facebook_event_checkin.csv facebook_event_checkin

-- get_fit_now_check_inテーブル
.mode csv
.import get_fit_now_check_in.csv get_fit_now_check_in

-- get_fit_now_memberテーブル
.mode csv
.import get_fit_now_member.csv get_fit_now_member

-- incomeテーブル
.mode csv
.import income.csv income

-- interviewテーブル
.mode csv
.import interview.csv interview

-- personテーブル
.mode csv
.import person.csv person

-- solutionテーブル
.mode csv
.import solution.csv solution

