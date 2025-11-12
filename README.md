# SQL殺人事件ミステリー

![証拠を調べる探偵のイラスト](174092-clue-illustration.png)

SQL市で殺人事件が発生しました！SQL殺人事件ミステリーは、SQLの概念とコマンドを学ぶための自習教材であり、同時に経験豊富なSQLユーザーが魅力的な事件を解決する楽しいゲームでもあります。

ミステリーを解決したい場合は、[mystery.knightlab.com](https://mystery.knightlab.com)にアクセスしてください。SQLが初めての場合は、[ウォークスルー](https://mystery.knightlab.com/walkthrough.html)から始めることをお勧めします。SQLのすべてを教えるわけではありませんが、ミステリーを解決するために必要なすべてのことを教えます。  

## 他に何がありますか？

ウェブベースのバージョンを構築する前に、これは人々が自分のコンピューターにダウンロードして解決できるように設計されていました。それに興味がある場合は、読み進めてください。

## 自分のコンピューターで解決するために必要なもの

* **sql-murder-mystery.db**: このSQLiteデータベースファイルには、作業するすべてのデータが含まれています。
* **プロンプト**: SQLの経験レベルに応じて、[prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf)ファイルまたは[prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf)ファイルのいずれかでプロンプトを見つけてください。
* **[リファレンス](https://github.com/NUKnightLab/sql-mysteries/blob/master/reference.pdf)**: これはSQLの概念とコマンドに関する速習コースです。
* **お好みのSQLite環境**: 初心者には、データを検査してクエリを記述するための優れたグラフィカルインターフェイスである[SQLiteStudio](https://sqlitestudio.pl/)の使用をお勧めします。

## 始め方

* **SQL初心者の方**: リファレンスから始めて、[prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf)ファイルを読み、次に[SQLiteStudioをインストールしてdbファイルを読み込む](https://github.com/NUKnightLab/sql-mysteries/blob/master/sqlite_studio.pdf)ことで始めます。途中で行き詰まった場合は、遠慮なくリファレンスを参照するか、[GitHub issue](https://github.com/NUKnightLab/sql-mysteries/issues)を提出して、どこで手順を改善する必要があるかをお知らせください。

* **SQL経験者の方**: [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf)ファイルを読み、次にsql-murder-mystery.dbファイルをダウンロードして、お好みのSQL環境を使用してミステリーを解決してください。SQLの記憶をリフレッシュするためにリファレンスを使用できます。SQL環境内ですべてのアクティビティを完了してみてください（メモを書き留めずに）！

## 解答の確認

正しい犯人を見つけたかどうかを確認するために、SQL環境で次のクエリを記述してください：

```SQL
INSERT INTO solution VALUES (1, "ここに見つけた人物の名前を入力してください");

SELECT value FROM solution;
```

## 作者

* [Joon Park](https://twitter.com/JoonParkMusic)
* [Cathy He](https://twitter.com/Cathy_MeiyingHe)

## インスピレーション

この殺人ミステリーは、[隣接するターミナル市での事件](https://github.com/veltman/clmystery "コマンドライン殺人ミステリー")に触発されました。

## 著作権とライセンス

このプロジェクトのオリジナルコードは[MITライセンス](https://github.com/NUKnightLab/sql-mysteries/blob/master/LICENSE)の下でリリースされています。

オリジナルテキストおよびその他のコンテンツは[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)の下でリリースされています。

ここで使用されているSQLクエリカスタムウェブコンポーネントは、[Select Star SQL](https://selectstarsql.com/)の作成者であるZi Chong Kaoによって作成され、パブリックドメインにリリースされたコードを適応したものです。

[rambleronによる探偵画像](https://www.vecteezy.com/vector-art/174092-clue-illustration)は、Vecteezyの無料ライセンスの下で使用されています。
