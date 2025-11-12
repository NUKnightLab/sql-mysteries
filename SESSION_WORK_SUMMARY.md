# SQL Murder Mystery 日本語化プロジェクト - 作業サマリー

## プロジェクト概要

SQL Murder Mystery（SQLを使った殺人ミステリーゲーム）を英語から日本語に翻訳するプロジェクト。
プレイヤーはSQLクエリを使って事件を調査し、犯人を特定します。

**リポジトリ:** rootassist/sql-mysteries-ja
**作業ブランチ:** claude/test-repository-access-011CV3y6a2SgHE4qGCAob7S6

---

## 完了した作業

### 1. walkthrough.htmlの翻訳 ✅

**ファイル:** `walkthrough.html`
**実施内容:**
- 17個のsql-exercise要素を翻訳
- `data-question`属性: 問題文を日本語化
- `data-comment`属性: ヒントを日本語化

**コミット:** 最初のコミット

---

### 2. データベース翻訳の準備 ✅

**ディレクトリ:** `conf/`
**実施内容:**

#### 2.1 CSV抽出（ユーザー実施済み）
- 元のデータベース（sql-murder-mystery.db）から8テーブルをCSV形式でエクスポート
- 合計56,650レコード

#### 2.2 翻訳マッピングの作成
**ファイル:** `conf/translation_mapping.json`
- カテゴリ値の翻訳定義（犯罪種別、色、性別、会員ステータス等）

#### 2.3 テキストデータのクリーニング
**ファイル:** `conf/clean_translation_files.py`
- CSVファイル内の改行コードを削除
- 翻訳作業を容易にするために空白に置換
- 出力: `*_translations_cleaned.csv` (3ファイル)

**生成ファイル:**
- `crime_scene_report_translations_cleaned.csv` (938件)
- `interview_translations_cleaned.csv` (3,098件)
- `facebook_event_checkin_translations_cleaned.csv` (902件)

---

### 3. ゲームフロー分析 ✅

**ファイル:** `conf/GAME_WALKTHROUGH.md`
**実施内容:**
- ゲームクリアまでの10ステップのSQLクエリを完全解析
- ゲームクリアに最低限必要なレコードを特定（6件）
- すべての探索パスを文書化

**重要な発見:**
- ゲームはSQLでの探索が重要
- 答えだけでなく探索過程を楽しむゲームデザイン
- ダミーデータ（不要な情報）も大量に含まれる

---

### 4. テキストデータの翻訳 ✅

**ユーザーによる翻訳:**
- `crime_scene_report_translations_cleaned.csv`: 938件翻訳
- `interview_translations_cleaned.csv`: 3,098件翻訳
- `facebook_event_checkin_translations_cleaned.csv`: 902件翻訳

**ファイル:** `conf/translate_database.py`
- 翻訳を元のCSVファイルに適用
- カテゴリ値の翻訳も適用
- 出力: `conf/ja/*.csv` (日本語テキスト版CSV)

**コミット:** 複数のコミットで段階的に実施

---

### 5. 列名翻訳の検討と決定 ✅

#### 5.1 翻訳ガイドの作成
**ファイル:** `conf/COLUMN_TRANSLATION_GUIDE.md`
- 全9テーブル・全列の翻訳案を提示
- 3つのアプローチを提案（最小限、積極的、ハイブリッド）
- 各列の役割と翻訳の影響を分析

#### 5.2 ユーザーによるカスタマイズ
**ファイル:** `conf/COLUMN_TRANSLATION_ISSUE.md`（ユーザーが作成）
- ユーザーが希望する列名翻訳を決定
- **ハイブリッド方式を採用:**
  - テーブル名: 日本語
  - 重要な列: 日本語
  - ID・キー列: 英語のまま
  - 固有名詞（name等）: 英語のまま

**コミット:** `dac347b データベース列名の日本語化検討ガイドを追加`

---

### 6. 日本語版データベースの生成 ✅

#### 6.1 列名マッピングの作成
**ファイル:** `conf/column_mapping.json`
- COLUMN_TRANSLATION_ISSUE.mdの内容をプログラム可能な形式に変換
- テーブル名と列名のマッピング定義

#### 6.2 日本語版スキーマの作成
**ファイル:** `conf/schema_ja.sql`
- 日本語のテーブル名・列名を使用したCREATE TABLE文
- 全9テーブルの定義

#### 6.3 データベース生成スクリプト
**ファイル:** `conf/create_japanese_database.py`
- CSVファイルの列名を日本語に変換
- 日本語列名のCSVを生成（`conf/ja_db/*.csv`）
- SQLiteデータベースを生成

**生成ファイル:**
- `conf/ja_db/*.csv`: 日本語列名のCSV（8ファイル）
- `conf/ja_db/sql-murder-mystery-ja.db`: 日本語版データベース
- `sql-murder-mystery-ja.db`: 同じファイル（リポジトリルートにコピー）

**動作確認:**
- ✅ テーブル名が日本語（9テーブル）
- ✅ SQL City殺人事件の検索クエリ動作
- ✅ 目撃者の検索クエリ動作
- ✅ 証言の取得クエリ動作
- ✅ 運転免許証の検索クエリ動作

**コミット:** `a83d61d 日本語版データベースを生成`（最新）

---

## 生成ファイル一覧

### ルートディレクトリ
```
sql-murder-mystery-ja.db          # 日本語版データベース（3.3MB、56,650レコード）
walkthrough.html                  # 翻訳済みウォークスルーページ
```

### conf/ ディレクトリ

#### データベース関連
```
column_mapping.json               # 列名マッピング定義
schema_ja.sql                     # 日本語版スキーマ
create_japanese_database.py       # データベース生成スクリプト
translate_database.py             # テキスト翻訳適用スクリプト
translation_mapping.json          # カテゴリ値翻訳定義
```

#### クリーニング・翻訳用
```
clean_translation_files.py        # CSVクリーニングスクリプト
crime_scene_report_translations_cleaned.csv    # 翻訳済み（938件）
interview_translations_cleaned.csv             # 翻訳済み（3,098件）
facebook_event_checkin_translations_cleaned.csv # 翻訳済み（902件）
```

#### 元のCSVファイル（英語版から抽出）
```
crime_scene_report.csv
drivers_license.csv
facebook_event_checkin.csv
get_fit_now_check_in.csv
get_fit_now_member.csv
income.csv
interview.csv
person.csv
```

#### 日本語テキスト版CSV（ja/）
```
ja/crime_scene_report.csv         # テキスト翻訳済み
ja/drivers_license.csv
ja/facebook_event_checkin.csv
ja/get_fit_now_check_in.csv
ja/get_fit_now_member.csv
ja/income.csv
ja/interview.csv
ja/person.csv
```

#### 日本語列名版CSV（ja_db/）
```
ja_db/crime_scene_report.csv      # テキスト＋列名が日本語
ja_db/drivers_license.csv
ja_db/facebook_event_checkin.csv
ja_db/get_fit_now_check_in.csv
ja_db/get_fit_now_member.csv
ja_db/income.csv
ja_db/interview.csv
ja_db/person.csv
ja_db/sql-murder-mystery-ja.db    # 最終的な日本語版データベース
```

#### ドキュメント
```
COLUMN_TRANSLATION_GUIDE.md       # 列名翻訳ガイド（提案）
COLUMN_TRANSLATION_ISSUE.md       # 列名翻訳決定版（ユーザー作成）
GAME_WALKTHROUGH.md               # ゲーム完全攻略フロー
```

---

## データベース構造

### テーブル一覧（日本語名）

| 英語名 | 日本語名 | レコード数 | 説明 |
|--------|----------|------------|------|
| crime_scene_report | 犯罪現場レポート | 1,228 | 犯罪記録 |
| drivers_license | 運転免許証 | 10,007 | 運転免許情報 |
| facebook_event_checkin | Facebookイベントチェックイン | 20,011 | イベント参加記録 |
| get_fit_now_check_in | GetFitNow入館記録 | 2,703 | ジム入館記録 |
| get_fit_now_member | GetFitNow会員情報 | 184 | ジム会員情報 |
| income | 収入情報 | 7,514 | 個人収入データ |
| interview | 証言 | 4,991 | 証言記録 |
| person | 人物情報 | 10,011 | 人物マスタ |
| solution | 正解 | 1 | ゲームの正解 |

### 列名の翻訳方針

**日本語化した列:**
- 日付: date → 発生日、誕生日、チェックイン日、イベント日
- 種別: type → 犯罪種別
- 内容: description → 事件内容
- 場所: city → 発生場所
- 身体特徴: gender → 性別、hair_color → 髪の色、eye_color → 目の色
- など（詳細は`conf/column_mapping.json`参照）

**英語のまま残した列:**
- すべてのID系: id, person_id, license_id, event_id, membership_id
- キー: ssn (社会保障番号)
- 固有名詞: name（人名は固有名詞として扱う）
- プレート番号: plate_number（車のナンバープレート）

---

## 使用方法

### 日本語版データベースのクエリ例

```sql
-- 1. ゲーム開始: SQL Cityの殺人事件を探す
SELECT * FROM 犯罪現場レポート
WHERE 犯罪種別 = '殺人' AND 発生場所 = 'SQL City';

-- 2. 目撃者を探す（ノースウェスタン通りの最後の家）
SELECT * FROM 人物情報
WHERE 住所_地名 LIKE '%Northwestern Dr%'
ORDER BY 住所_番地 DESC LIMIT 1;

-- 3. 証言を確認
SELECT 証言内容 FROM 証言 WHERE person_id = 14887;

-- 4. 容疑者の運転免許証を探す
SELECT * FROM 運転免許証
WHERE 性別 = 'male'
  AND 髪の色 = 'red'
  AND 身長 BETWEEN 65 AND 67;

-- 5. 運転免許証から人物を特定
SELECT p.name, p.id
FROM 人物情報 p
JOIN 運転免許証 d ON p.license_id = d.id
WHERE d.plate_number LIKE '%H42W%';
```

### データベースの再生成方法

元のCSVファイルを修正した場合、以下のコマンドでデータベースを再生成できます：

```bash
cd /home/user/sql-mysteries-ja/conf
python3 create_japanese_database.py
```

---

## 残っている作業

### 必須作業
現時点で必須の作業はありません。基本的な日本語化は完了しています。

### オプション作業（今後の改善案）

#### 1. walkthrough.htmlの動作確認
- [ ] ブラウザで開いて日本語版データベースが正しく読み込まれるか確認
- [ ] 各sql-exerciseが日本語クエリで動作するか確認
- [ ] 必要に応じてHTMLファイル内のサンプルクエリを更新

#### 2. index.htmlやprompt_beginner.htmlの翻訳
- [ ] ゲームのメインページ（index.html）の翻訳
- [ ] 初心者向けガイド（prompt_beginner.html）の翻訳
- [ ] その他のHTMLファイルの確認と翻訳

#### 3. READMEの更新
- [ ] 日本語版の使い方をREADMEに追加
- [ ] 英語版と日本語版の切り替え方法を記載
- [ ] データベースの再生成方法を記載

#### 4. ウェブアプリケーションの設定
- [ ] HTMLファイルが日本語版データベース（sql-murder-mystery-ja.db）を読み込むように設定変更
- [ ] データベースパスの確認と修正

#### 5. テスト
- [ ] ゲーム全体を通してプレイして日本語化の品質確認
- [ ] 各クエリが正常に動作するか確認
- [ ] 誤訳や不自然な表現の修正

#### 6. ドキュメント整備
- [ ] 日本語版プレイガイドの作成
- [ ] SQLチュートリアルの日本語化
- [ ] よくある質問（FAQ）の作成

---

## 技術メモ

### 使用技術
- **データベース:** SQLite 3
- **言語:** Python 3
- **ファイル形式:** CSV (UTF-8)
- **エンコーディング:** UTF-8 (BOM付きの場合は自動除去)

### 重要な設計判断

1. **ハイブリッド翻訳方式**
   - テーブル名・重要列名: 日本語
   - ID・キー: 英語
   - 理由: SQLの読みやすさと、ID列は変換不要との判断

2. **改行の除去**
   - 元のCSVにあった改行コードを空白に置換
   - 理由: スプレッドシートでの翻訳作業を容易にするため

3. **3段階のCSV変換**
   - 元CSV → テキスト翻訳版（ja/） → 列名翻訳版（ja_db/）
   - 理由: 各段階で確認・修正が可能

### トラブルシューティング

**問題:** CSVファイルに改行が含まれて列が抽出できない
**解決:** `clean_translation_files.py`で改行を空白に置換

**問題:** 翻訳がCSVに適用されない
**解決:** `translate_database.py`で元テキストをクリーニングしてから比較

**問題:** UTF-8 BOMがある
**解決:** スクリプトで自動的にBOMを除去（utf-8-sig）

---

## 参考リンク

- **元のゲーム:** [SQL Murder Mystery](https://mystery.knightlab.com/)
- **リポジトリ:** rootassist/sql-mysteries-ja
- **作業ブランチ:** claude/test-repository-access-011CV3y6a2SgHE4qGCAob7S6

---

## セッション情報

**最終更新:** 2025-11-12
**最終コミット:** a83d61d 日本語版データベースを生成
**ブランチ:** claude/test-repository-access-011CV3y6a2SgHE4qGCAob7S6
**ステータス:** 基本的な日本語化完了、プッシュ済み

---

## 次のセッションで確認すべきこと

1. `walkthrough.html`がブラウザで正しく動作するか
2. 日本語版データベースがHTMLから正しく読み込まれるか
3. 他のHTMLファイル（index.html等）の翻訳が必要か
4. READMEに日本語版の使用方法を追加する必要があるか

---

このドキュメントは作業の引き継ぎ用です。次のセッションでこのファイルを参照してください。
