#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻訳用CSVファイルから改行を削除し、半角スペースに置き換えるスクリプト
"""

import csv
import re

def clean_text(text):
    """
    テキストから改行を削除し、半角スペースに置き換える
    複数の連続したスペースは1つにまとめる
    """
    # 改行を半角スペースに置き換え
    text = text.replace('\n', ' ').replace('\r', ' ')

    # タブも半角スペースに置き換え
    text = text.replace('\t', ' ')

    # 複数の連続したスペースを1つにまとめる
    text = re.sub(r'\s+', ' ', text)

    # 前後の空白を削除
    text = text.strip()

    return text

def clean_csv_file(input_file, output_file, text_column):
    """
    CSVファイルの指定された列から改行を削除する
    """
    print(f"処理中: {input_file}")

    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            # テキスト列をクリーンアップ
            row[text_column] = clean_text(row[text_column])
            rows.append(row)

    # クリーンアップしたデータを保存
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  → {output_file} に保存しました")
    print(f"  → {len(rows)} 件を処理しました")

def main():
    """メイン処理"""
    print("=" * 60)
    print("翻訳用CSVファイルのクリーンアップ")
    print("=" * 60)
    print()

    # 各ファイルをクリーンアップ
    clean_csv_file(
        'translation_descriptions.csv',
        'translation_descriptions_cleaned.csv',
        'original'
    )
    print()

    clean_csv_file(
        'translation_transcripts.csv',
        'translation_transcripts_cleaned.csv',
        'original'
    )
    print()

    clean_csv_file(
        'translation_events.csv',
        'translation_events_cleaned.csv',
        'original'
    )
    print()

    print("=" * 60)
    print("クリーンアップ完了！")
    print("以下のファイルが生成されました:")
    print("  - translation_descriptions_cleaned.csv")
    print("  - translation_transcripts_cleaned.csv")
    print("  - translation_events_cleaned.csv")
    print("=" * 60)

if __name__ == '__main__':
    main()
