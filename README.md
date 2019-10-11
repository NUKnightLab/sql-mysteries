# SQL Murder Mystery

![Illustration of a detective looking at evidence](174092-clue-illustration.png)

There's been a Murder in SQL City! The SQL Murder Mystery is designed to be both a self-directed lesson to learn SQL concepts and commands and a fun game for experienced SQL users to solve an intriguing crime.

## What You Need

**Nothing more than a web browser!** You can now solve the mystery in your browser, by going to [mystery.knightlab.com](http://mystery.knightlab.com). If you're new to SQL, you may want to start at [our walkthrough](http://mystery.knightlab.com/walkthrough.html). It won't teach you everything about SQL, but it should teach you all that you need to solve the mystery.

Before we developed the web-based version, we designed this for people to download and solve on their own. If you're interested in that, read on:

* **sql-murder-mystery.db**: This SQLite database file contains all the data that you will be working with.
* **prompt**: Depending on your experience level with SQL, find the prompt in either the [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) file or the [prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) file.
* **[reference](https://github.com/NUKnightLab/sql-mysteries/blob/master/reference.pdf)**: This is a crash course on SQL concepts and commands.
* **a SQLite environment of your choice**: For beginners, we recommend using [SQLiteStudio](https://sqlitestudio.pl/index.rvt), which is a good graphical interface to use to inspect your data and write queries.

**NEW:** If you don't want to install anything, you can query [a web-based version of the database](https://sql-murder-mystery.datasette.io/sql-murder-mystery) published by [Simon Willison](https://simonwillison.net/) using his awesome [Datasette](https://datasette.readthedocs.io/) tool. If you do that, just download the  [beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) or [experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) prompt file and get started.

## Getting Started
* **For SQL beginners**: start with the reference, read the [prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) file, then get started by [installing SQLiteStudio and loading the db file](https://github.com/NUKnightLab/sql-mysteries/blob/master/sqlite_studio.pdf). If you get stuck at any point, feel free to refer back to the reference, or file a [GitHub issue](https://github.com/NUKnightLab/sql-mysteries/issues) so we can know where our instructions need to be improved.

* **For experienced SQL users**: read the [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) file, then download the sql-murder-mystery.db file and use a SQL environment of your choice to solve the mystery. You can use the reference to refresh your memory of SQL. Try to complete the activity all within your SQL environment (without writing down notes)!


## Checking the Solution
Write the following queries in your SQL environment to check whether you've found the right murderer:

```SQL
INSERT INTO solution VALUES (1, "Insert the name of the person you found here");

SELECT value FROM solution;
```


## Authors
Joon Park

Cathy He

## Inspiration
This murder mystery was inspired by [a crime in the neighboring Terminal City](https://github.com/veltman/clmystery "command-line murder mystery").
