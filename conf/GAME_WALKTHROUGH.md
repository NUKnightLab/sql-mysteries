# SQL Murder Mystery ゲーム攻略フロー

このドキュメントは、ゲームをクリアするためにプレイヤーが実行する必要があるSQLクエリの流れを示しています。

## ゲームの目標

1. SQL City で発生した殺人事件の犯人を特定する
2. さらに、事件の黒幕を特定する

---

## 攻略フロー

### ステップ1: 最初の手がかりを見つける

**プレイヤーが実行するSQL:**
```sql
SELECT * FROM crime_scene_report
WHERE type = 'murder' AND city = 'SQL City';
```

**結果:** 3件の殺人事件レポートが表示される
- **重要:** 2018-01-15 の事件レポートに目撃者2人の情報が含まれている

**翻訳が必要なデータ:**
- `description` ID: 1227, 3, 4

---

### ステップ2: 目撃者1を特定する

**手がかり:** "Northwestern Dr" の最後の家に住んでいる

**プレイヤーが実行するSQL:**
```sql
SELECT * FROM person
WHERE address_street_name = 'Northwestern Dr'
ORDER BY address_number DESC
LIMIT 1;
```

**結果:** Morty Schapiro (person_id: 14887)

---

### ステップ3: 目撃者2を特定する

**手がかり:** 名前に "Annabel" が含まれ、"Franklin Ave" に住んでいる

**プレイヤーが実行するSQL:**
```sql
SELECT * FROM person
WHERE name LIKE '%Annabel%'
  AND address_street_name = 'Franklin Ave';
```

**結果:** Annabel Miller (person_id: 16371)

---

### ステップ4: 目撃者のインタビューを読む

**プレイヤーが実行するSQL:**
```sql
SELECT p.name, i.transcript
FROM interview i
JOIN person p ON i.person_id = p.id
WHERE i.person_id IN (14887, 16371);
```

**結果:** 2件のインタビュー
- **Morty Schapiro:** ジムバッグ、会員番号 "48Z"、ゴールド会員、車のナンバーに "H42W" が含まれる
- **Annabel Miller:** 1月9日にジムで犯人を見た

**翻訳が必要なデータ:**
- `transcript` ID: 4988 (Morty Schapiro)
- `transcript` ID: 4989 (Annabel Miller)

---

### ステップ5: 容疑者を絞り込む（ジム会員）

**手がかり:** 会員番号が "48Z" で始まるゴールド会員

**プレイヤーが実行するSQL:**
```sql
SELECT * FROM get_fit_now_member
WHERE id LIKE '48Z%'
  AND membership_status = 'gold';
```

**結果:** 2人の容疑者
- Joe Germuska (会員ID: 48Z7A, person_id: 28819)
- Jeremy Bowers (会員ID: 48Z55, person_id: 67318)

---

### ステップ6: 1月9日のジム記録を確認

**プレイヤーが実行するSQL:**
```sql
SELECT * FROM get_fit_now_check_in
WHERE check_in_date = 20180109
  AND membership_id LIKE '48Z%';
```

**結果:** 両方とも1月9日にジムにいた
- 48Z7A: 16:00-17:30
- 48Z55: 15:30-17:00

---

### ステップ7: 車のナンバーから犯人を特定

**手がかり:** ナンバープレートに "H42W" が含まれる

**プレイヤーが実行するSQL:**
```sql
SELECT p.name, dl.plate_number, dl.car_make, dl.car_model
FROM person p
JOIN drivers_license dl ON p.license_id = dl.id
WHERE p.id IN (28819, 67318)
  AND dl.plate_number LIKE '%H42W%';
```

**結果:** **Jeremy Bowers** が犯人
- 車: Chevrolet Spark LS
- ナンバー: 0H42W2

---

### ステップ8: 犯人のインタビューを読む

**プレイヤーが実行するSQL:**
```sql
SELECT * FROM interview
WHERE person_id = 67318;
```

**結果:** 黒幕の存在が判明
- 女性
- 身長: 5'5"〜5'7" (65〜67インチ)
- 赤い髪
- Tesla Model S
- 2017年12月に SQL Symphony Concert に3回出席

**翻訳が必要なデータ:**
- `transcript` ID: 4990 (Jeremy Bowers)

---

### ステップ9: 黒幕を特定する（運転免許証から）

**プレイヤーが実行するSQL:**
```sql
SELECT p.id, p.name, dl.*
FROM person p
JOIN drivers_license dl ON p.license_id = dl.id
WHERE dl.gender = 'female'
  AND dl.height BETWEEN 65 AND 67
  AND dl.hair_color = 'red'
  AND dl.car_make = 'Tesla'
  AND dl.car_model = 'Model S';
```

**結果:** 3人の候補
- Red Korb (ID: 78881)
- Regina George (ID: 90700)
- Miranda Priestly (ID: 99716)

---

### ステップ10: コンサート参加記録から黒幕を特定

**プレイヤーが実行するSQL:**
```sql
SELECT person_id, event_name, COUNT(*) as concert_count
FROM facebook_event_checkin
WHERE person_id IN (78881, 90700, 99716)
  AND event_name LIKE '%SQL Symphony Concert%'
  AND date BETWEEN 20171201 AND 20171231
GROUP BY person_id;
```

**結果:** **Miranda Priestly** (person_id: 99716) が黒幕
- コンサート参加回数: 3回

---

## 答えの確認

**プレイヤーが実行するSQL:**
```sql
INSERT INTO solution VALUES (1, 'Jeremy Bowers');
SELECT value FROM solution;
```

```sql
INSERT INTO solution VALUES (1, 'Miranda Priestly');
SELECT value FROM solution;
```

---

## 翻訳が必要なデータのまとめ

### crime_scene_report.description
- ID 1227: Security footage shows that there were 2 witnesses...
- ID 3: REDACTED REDACTED REDACTED
- ID 4: Someone killed the guard! He took an arrow to the knee!

### interview.transcript
- ID 4988 (Morty Schapiro): I heard a gunshot and then saw a man run out...
- ID 4989 (Annabel Miller): I saw the murder happen, and I recognized the killer...
- ID 4990 (Jeremy Bowers): I was hired by a woman with a lot of money...

### カテゴリ値（既に翻訳済み）
- crime_types: murder → 殺人
- gender: male → 男性, female → 女性
- hair_color: red → 赤
- membership_status: gold → ゴールド

---

## 注意事項

- プレイヤーは探索の過程で他のデータも見る可能性がある
- ダミーデータ（Alice in Wonderlandの引用など）は翻訳不要
- 最小限の翻訳でゲームはプレイ可能だが、完全な体験には追加の翻訳が望ましい
