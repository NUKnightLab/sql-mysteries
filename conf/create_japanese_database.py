#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本語版データベース生成スクリプト

COLUMN_TRANSLATION_ISSUE.md に基づいて列名を日本語化し、
日本語版SQLiteデータベースを生成します。
"""

import csv
import json
import os
import sqlite3

def load_column_mapping():
    """列名マッピングをJSONファイルから読み込む"""
    with open('column_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def rename_csv_columns(input_file, output_file, column_map):
    """CSVファイルの列名を日本語化"""
    print(f"  処理中: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as fin:
        reader = csv.DictReader(fin)
        rows = list(reader)

        if not rows:
            print(f"    ⚠️ データなし")
            return

        # 列名を日本語化
        old_fieldnames = reader.fieldnames
        new_fieldnames = [column_map.get(col, col) for col in old_fieldnames]

        # データを新しい列名でマッピング
        new_rows = []
        for row in rows:
            new_row = {}
            for old_col, new_col in zip(old_fieldnames, new_fieldnames):
                new_row[new_col] = row[old_col]
            new_rows.append(new_row)

    # 出力
    with open(output_file, 'w', encoding='utf-8', newline='') as fout:
        writer = csv.DictWriter(fout, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"    → {output_file} に保存 ({len(new_rows)} 件)")

def create_japanese_csvs():
    """日本語版CSVファイルを生成"""
    print("=" * 70)
    print("日本語版CSVファイルの生成")
    print("=" * 70)
    print()

    # 列名マッピングを読み込み
    mapping = load_column_mapping()

    # 出力ディレクトリを作成
    os.makedirs('ja_db', exist_ok=True)

    # 各テーブルのCSVファイルを処理
    tables = [
        'crime_scene_report',
        'drivers_license',
        'facebook_event_checkin',
        'get_fit_now_check_in',
        'get_fit_now_member',
        'income',
        'interview',
        'person',
        'solution'
    ]

    for table in tables:
        input_file = f'ja/{table}.csv'
        output_file = f'ja_db/{table}.csv'
        column_map = mapping['column_names'].get(table, {})

        if os.path.exists(input_file):
            rename_csv_columns(input_file, output_file, column_map)
        else:
            print(f"  ⚠️ {input_file} が見つかりません")

    print()
    print("=" * 70)
    print("CSVファイルの生成完了")
    print("=" * 70)

def create_sqlite_database():
    """日本語版SQLiteデータベースを生成"""
    print()
    print("=" * 70)
    print("SQLiteデータベースの生成")
    print("=" * 70)
    print()

    db_file = 'ja_db/sql-murder-mystery-ja.db'

    # 既存のデータベースファイルを削除
    if os.path.exists(db_file):
        os.remove(db_file)

    # データベースを作成
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # スキーマを読み込んで実行
    print("  スキーマを作成中...")
    with open('schema_ja.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)

    # 列名マッピングを読み込み
    mapping = load_column_mapping()

    # 各テーブルにデータをインポート
    tables = [
        ('犯罪現場レポート', 'crime_scene_report'),
        ('運転免許証', 'drivers_license'),
        ('Facebookイベント参加記録', 'facebook_event_checkin'),
        ('ジムチェックイン記録', 'get_fit_now_check_in'),
        ('ジム会員情報', 'get_fit_now_member'),
        ('年収', 'income'),
        ('証言', 'interview'),
        ('人物情報', 'person'),
        ('解答', 'solution')
    ]

    for ja_table_name, en_table_name in tables:
        csv_file = f'ja_db/{en_table_name}.csv'

        if not os.path.exists(csv_file):
            print(f"  ⚠️ {csv_file} が見つかりません")
            continue

        print(f"  データをインポート中: {ja_table_name}...")

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            if not rows:
                print(f"    データなし")
                continue

            # 列名を取得
            columns = reader.fieldnames
            placeholders = ','.join(['?' for _ in columns])
            column_names = ','.join([f'`{col}`' for col in columns])

            # データを挿入
            insert_sql = f'INSERT INTO `{ja_table_name}` ({column_names}) VALUES ({placeholders})'

            for row in rows:
                values = [row[col] for col in columns]
                cursor.execute(insert_sql, values)

            print(f"    → {len(rows)} 件を挿入")

    conn.commit()
    conn.close()

    print()
    print(f"  ✅ データベースを作成しました: {db_file}")
    print()
    print("=" * 70)
    print("データベース生成完了")
    print("=" * 70)

def main():
    """メイン処理"""
    print()
    print("=" * 70)
    print("SQL Murder Mystery 日本語版データベース生成")
    print("=" * 70)
    print()

    # ステップ1: 日本語版CSVファイルを生成
    create_japanese_csvs()

    # ステップ2: SQLiteデータベースを生成
    create_sqlite_database()

    print()
    print("=" * 70)
    print("すべての処理が完了しました！")
    print("=" * 70)
    print()
    print("生成されたファイル:")
    print("  - ja_db/*.csv (列名が日本語化されたCSVファイル)")
    print("  - ja_db/sql-murder-mystery-ja.db (日本語版SQLiteデータベース)")
    print()

if __name__ == '__main__':
    main()
