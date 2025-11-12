-- SQL Murder Mystery 日本語版データベーススキーマ
-- COLUMN_TRANSLATION_ISSUE.md に基づく列名の日本語化

-- Table: 犯罪現場レポート (crime_scene_report)
CREATE TABLE 犯罪現場レポート (
        発生日 integer,
        犯罪種別 text,
        事件内容 text,
        発生場所 text
    );

-- Table: 運転免許証 (drivers_license)
CREATE TABLE 運転免許証 (
        id integer PRIMARY KEY,
        年齢 integer,
        身長 integer,
        目の色 text,
        髪の色 text,
        性別 text,
        自動車ナンバー text,
        自動車メーカー text,
        自動車モデル text
    );

-- Table: Facebookイベント参加記録 (facebook_event_checkin)
CREATE TABLE Facebookイベント参加記録 (
        person_id integer,
        event_id integer,
        イベント名 text,
        参加日 integer,
        FOREIGN KEY (person_id) REFERENCES 人物情報(id)
    );

-- Table: ジムチェックイン記録 (get_fit_now_check_in)
CREATE TABLE ジムチェックイン記録 (
        membership_id text,
        チェックイン日 integer,
        チェックイン時刻 integer,
        チェックアウト時刻 integer,
        FOREIGN KEY (membership_id) REFERENCES ジム会員情報(id)
    );

-- Table: ジム会員情報 (get_fit_now_member)
CREATE TABLE ジム会員情報 (
        id text PRIMARY KEY,
        person_id integer,
        name text,
        会員開始日 integer,
        会員ランク text,
        FOREIGN KEY (person_id) REFERENCES 人物情報(id)
    );

-- Table: 年収 (income)
CREATE TABLE 年収 (
        ssn CHAR PRIMARY KEY,
        年収額 integer
    );

-- Table: 証言 (interview)
CREATE TABLE 証言 (
        person_id integer,
        証言内容 text,
        FOREIGN KEY (person_id) REFERENCES 人物情報(id)
    );

-- Table: 人物情報 (person)
CREATE TABLE 人物情報 (
        id integer PRIMARY KEY,
        name text,
        license_id integer,
        番地 integer,
        通り名 text,
        ssn CHAR REFERENCES 年収(ssn),
        FOREIGN KEY (license_id) REFERENCES 運転免許証(id)
    );

-- Table: 解答 (solution)
CREATE TABLE 解答 (
        プレーヤー番号 integer,
        犯人の名前 text
    );
