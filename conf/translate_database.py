#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Murder Mystery データベース翻訳スクリプト

使用方法:
    python3 translate_database.py

出力:
    - 翻訳されたCSVファイルが ja/ ディレクトリに生成されます
"""

import csv
import json
import os
from pathlib import Path

def load_translation_mapping():
    """翻訳マッピングをJSONファイルから読み込む"""
    with open('translation_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_text_translations(filename):
    """テキスト翻訳CSVを読み込む（存在する場合）"""
    translations = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['japanese']:  # 日本語訳がある場合のみ
                    translations[row['original']] = row['japanese']
    return translations

def translate_crime_scene_report(mapping, text_translations):
    """crime_scene_report.csv を翻訳"""
    print("crime_scene_report.csv を翻訳中...")

    input_file = 'crime_scene_report.csv'
    output_file = 'ja/crime_scene_report.csv'

    with open(input_file, 'r', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        rows = []

        for row in reader:
            # type を翻訳
            if row['type'] in mapping['crime_types']:
                row['type'] = mapping['crime_types'][row['type']]

            # description を翻訳（翻訳がある場合）
            if row['description'] in text_translations:
                row['description'] = text_translations[row['description']]

            rows.append(row)

    # 出力
    with open(output_file, 'w', encoding='utf-8', newline='') as fout:
        if rows:
            writer = csv.DictWriter(fout, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"  → {output_file} に保存しました")

def translate_drivers_license(mapping):
    """drivers_license.csv を翻訳"""
    print("drivers_license.csv を翻訳中...")

    input_file = 'drivers_license.csv'
    output_file = 'ja/drivers_license.csv'

    with open(input_file, 'r', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        rows = []

        for row in reader:
            # gender を翻訳
            if row['gender'] in mapping['gender']:
                row['gender'] = mapping['gender'][row['gender']]

            # eye_color を翻訳
            if row['eye_color'] in mapping['eye_color']:
                row['eye_color'] = mapping['eye_color'][row['eye_color']]

            # hair_color を翻訳
            if row['hair_color'] in mapping['hair_color']:
                row['hair_color'] = mapping['hair_color'][row['hair_color']]

            rows.append(row)

    # 出力
    with open(output_file, 'w', encoding='utf-8', newline='') as fout:
        if rows:
            writer = csv.DictWriter(fout, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"  → {output_file} に保存しました")

def translate_interview(text_translations):
    """interview.csv を翻訳"""
    print("interview.csv を翻訳中...")

    input_file = 'interview.csv'
    output_file = 'ja/interview.csv'

    with open(input_file, 'r', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        rows = []

        for row in reader:
            # transcript を翻訳（翻訳がある場合）
            if row['transcript'] in text_translations:
                row['transcript'] = text_translations[row['transcript']]

            rows.append(row)

    # 出力
    with open(output_file, 'w', encoding='utf-8', newline='') as fout:
        if rows:
            writer = csv.DictWriter(fout, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"  → {output_file} に保存しました")

def translate_facebook_event_checkin(text_translations):
    """facebook_event_checkin.csv を翻訳"""
    print("facebook_event_checkin.csv を翻訳中...")

    input_file = 'facebook_event_checkin.csv'
    output_file = 'ja/facebook_event_checkin.csv'

    with open(input_file, 'r', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        rows = []

        for row in reader:
            # event_name を翻訳（翻訳がある場合）
            if row['event_name'] in text_translations:
                row['event_name'] = text_translations[row['event_name']]

            rows.append(row)

    # 出力
    with open(output_file, 'w', encoding='utf-8', newline='') as fout:
        if rows:
            writer = csv.DictWriter(fout, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"  → {output_file} に保存しました")

def translate_get_fit_now_member(mapping):
    """get_fit_now_member.csv を翻訳"""
    print("get_fit_now_member.csv を翻訳中...")

    input_file = 'get_fit_now_member.csv'
    output_file = 'ja/get_fit_now_member.csv'

    with open(input_file, 'r', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        rows = []

        for row in reader:
            # membership_status を翻訳
            if row['membership_status'] in mapping['membership_status']:
                row['membership_status'] = mapping['membership_status'][row['membership_status']]

            rows.append(row)

    # 出力
    with open(output_file, 'w', encoding='utf-8', newline='') as fout:
        if rows:
            writer = csv.DictWriter(fout, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"  → {output_file} に保存しました")

def copy_unchanged_files():
    """変更不要なファイルをそのままコピー"""
    print("変更不要なファイルをコピー中...")

    unchanged_files = [
        'person.csv',
        'income.csv',
        'get_fit_now_check_in.csv',
        'solution.csv'
    ]

    for filename in unchanged_files:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8-sig') as fin:
                content = fin.read()
            with open(f'ja/{filename}', 'w', encoding='utf-8') as fout:
                fout.write(content)
            print(f"  → ja/{filename} にコピーしました")

def main():
    """メイン処理"""
    print("=" * 60)
    print("SQL Murder Mystery データベース翻訳スクリプト")
    print("=" * 60)
    print()

    # 出力ディレクトリを作成
    os.makedirs('ja', exist_ok=True)

    # 翻訳マッピングを読み込み
    print("翻訳マッピングを読み込んでいます...")
    mapping = load_translation_mapping()
    print(f"  ✓ カテゴリ値の翻訳マッピングを読み込みました")
    print()

    # テキスト翻訳を読み込み
    print("テキスト翻訳を読み込んでいます...")
    desc_translations = load_text_translations('translation_descriptions.csv')
    transcript_translations = load_text_translations('translation_transcripts.csv')
    event_translations = load_text_translations('translation_events.csv')
    print(f"  ✓ description: {len(desc_translations)} 件")
    print(f"  ✓ transcript: {len(transcript_translations)} 件")
    print(f"  ✓ event_name: {len(event_translations)} 件")
    print()

    # 各ファイルを翻訳
    print("CSVファイルを翻訳しています...")
    print()
    translate_crime_scene_report(mapping, desc_translations)
    translate_drivers_license(mapping)
    translate_interview(transcript_translations)
    translate_facebook_event_checkin(event_translations)
    translate_get_fit_now_member(mapping)
    copy_unchanged_files()

    print()
    print("=" * 60)
    print("翻訳完了！")
    print("翻訳されたファイルは ja/ ディレクトリに保存されました")
    print("=" * 60)

if __name__ == '__main__':
    main()
