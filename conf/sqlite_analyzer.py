import sqlite3
import csv
import os
from pathlib import Path

class SQLiteAnalyzer:
    def __init__(self, db_path, output_dir='output'):
        """
        SQLiteデータベースを解析してCSVとSQL文を生成

        Args:
            db_path: データベースファイルのパス
            output_dir: 出力ディレクトリ
        """
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_tables(self):
        """テーブル一覧を取得"""
        self.cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_schema(self, table_name):
        """テーブルのスキーマ情報を取得"""
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()

        # CREATE TABLE文を取得
        self.cursor.execute("""
            SELECT sql FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table_name,))
        create_sql = self.cursor.fetchone()[0]

        return {
            'columns': columns,
            'create_sql': create_sql
        }

    def export_table_to_csv(self, table_name):
        """テーブルをCSVにエクスポート"""
        # データを取得
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()

        # 列名を取得
        column_names = [description[0] for description in self.cursor.description]

        # CSVファイルに書き込み
        csv_path = self.output_dir / f"{table_name}.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)  # ヘッダー
            writer.writerows(rows)

        return csv_path, len(rows)

    def generate_schema_file(self):
        """すべてのテーブルのスキーマをファイルに出力"""
        schema_path = self.output_dir / "schema.sql"

        with open(schema_path, 'w', encoding='utf-8') as f:
            tables = self.get_tables()

            for table in tables:
                schema = self.get_table_schema(table)
                f.write(f"-- Table: {table}\n")
                f.write(f"{schema['create_sql']};\n\n")

                # 列情報も記載
                f.write(f"-- Columns for {table}:\n")
                for col in schema['columns']:
                    cid, name, col_type, notnull, dflt_value, pk = col
                    f.write(f"--   {name}: {col_type}")
                    if pk:
                        f.write(" (PRIMARY KEY)")
                    if notnull:
                        f.write(" NOT NULL")
                    if dflt_value:
                        f.write(f" DEFAULT {dflt_value}")
                    f.write("\n")
                f.write("\n")

            # インデックス情報
            self.cursor.execute("""
                SELECT sql FROM sqlite_master
                WHERE type='index' AND sql IS NOT NULL
            """)
            indexes = self.cursor.fetchall()

            if indexes:
                f.write("\n-- Indexes\n")
                for idx in indexes:
                    f.write(f"{idx[0]};\n")

        return schema_path

    def generate_import_script(self):
        """CSVインポート用のSQLスクリプトを生成"""
        import_path = self.output_dir / "import_data.sql"
        tables = self.get_tables()

        with open(import_path, 'w', encoding='utf-8') as f:
            f.write("-- CSVファイルからデータをインポートするスクリプト\n")
            f.write("-- 使用方法: sqlite3 new_database.db < import_data.sql\n\n")

            for table in tables:
                f.write(f"-- {table}テーブル\n")
                f.write(f".mode csv\n")
                f.write(f".import {table}.csv {table}\n\n")

        return import_path

    def analyze_and_export(self):
        """完全な解析とエクスポートを実行"""
        print(f"データベース解析開始: {self.db_path}")
        print(f"出力先: {self.output_dir}\n")

        # テーブル一覧
        tables = self.get_tables()
        print(f"テーブル数: {len(tables)}")
        print(f"テーブル: {', '.join(tables)}\n")

        # スキーマ出力
        schema_path = self.generate_schema_file()
        print(f"✓ スキーマファイル作成: {schema_path}")

        # 各テーブルをCSVにエクスポート
        print("\nCSVエクスポート:")
        for table in tables:
            csv_path, row_count = self.export_table_to_csv(table)
            print(f"  ✓ {table}: {row_count}行 → {csv_path}")

        # インポートスクリプト生成
        import_path = self.generate_import_script()
        print(f"\n✓ インポートスクリプト作成: {import_path}")

        # サマリーファイル作成
        self.generate_summary()

        print("\n完了！次のステップ:")
        print("1. output/フォルダ内のCSVファイルで翻訳が必要な箇所を確認")
        print("2. 必要に応じてCSVを編集")
        print("3. schema.sqlで列名などを翻訳")
        print("4. 新しいデータベースを作成してインポート")

    def generate_summary(self):
        """サマリーファイルを生成"""
        summary_path = self.output_dir / "README.txt"
        tables = self.get_tables()

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("SQLiteデータベース解析結果\n")
            f.write("=" * 50 + "\n\n")

            for table in tables:
                schema = self.get_table_schema(table)
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]

                f.write(f"テーブル: {table}\n")
                f.write(f"行数: {count}\n")
                f.write(f"列:\n")
                for col in schema['columns']:
                    cid, name, col_type, notnull, dflt_value, pk = col
                    f.write(f"  - {name} ({col_type})\n")
                f.write("\n")

    def close(self):
        """データベース接続を閉じる"""
        self.conn.close()


if __name__ == "__main__":
    # 使用例
    db_file = "sql-murder-mystery.db"  # ここにデータベースファイル名を指定

    if not os.path.exists(db_file):
        print(f"エラー: {db_file} が見つかりません")
        print("db_file変数に正しいパスを指定してください")
    else:
        analyzer = SQLiteAnalyzer(db_file, output_dir='output')
        try:
            analyzer.analyze_and_export()
        finally:
            analyzer.close()
