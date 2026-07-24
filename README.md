# SQL Murder Mystery

![Illustration of a detective looking at evidence](174092-clue-illustration.png)

There's been a Murder in SQL City! The SQL Murder Mystery is designed to be both a self-directed lesson to learn SQL concepts and commands and a fun game for experienced SQL users to solve an intriguing crime.

If you just want to solve the mystery, go to [mystery.knightlab.com](https://mystery.knightlab.com). If you're new to SQL, you may want to start at [our walkthrough](https://mystery.knightlab.com/walkthrough.html). It won't teach you everything about SQL, but it should teach you all that you need to solve the mystery.  

## What Else is Here?

Before we built the web-based version, we designed this for people to download and solve on their own computer. If you're interested in that, read on.

## What you need to solve on your own computer

* **sql-murder-mystery.db**: This SQLite database file contains all the data that you will be working with.
* **prompt**: Depending on your experience level with SQL, find the prompt in either the [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) file or the [prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) file.
* **[reference](https://github.com/NUKnightLab/sql-mysteries/blob/master/reference.pdf)**: This is a crash course on SQL concepts and commands.
* **a SQLite environment of your choice**: For beginners, we recommend using [SQLiteStudio](https://sqlitestudio.pl/), which is a good graphical interface to use to inspect your data and write queries.

## Getting Started
* **For SQL beginners**: start with the reference, read the [prompt_beginner](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_beginner.pdf) file, then get started by [installing SQLiteStudio and loading the db file](https://github.com/NUKnightLab/sql-mysteries/blob/master/sqlite_studio.pdf). If you get stuck at any point, feel free to refer back to the reference, or file a [GitHub issue](https://github.com/NUKnightLab/sql-mysteries/issues) so we can know where our instructions need to be improved.

* **For experienced SQL users**: read the [prompt_experienced](https://github.com/NUKnightLab/sql-mysteries/blob/master/prompt_experienced.pdf) file, then download the sql-murder-mystery.db file and use a SQL environment of your choice to solve the mystery. You can use the reference to refresh your memory of SQL. Try to complete the activity all within your SQL environment (without writing down notes)!


## Checking the Solution
Write the following queries in your SQL environment to check whether you've found the right murderer:

```SQL
INSERT INTO solution VALUES (1, "Insert the name of the person you found here");

SELECT value FROM solution;
```

## Letting an AI Agent Play

The repository includes two command-line, tool-using agents. Both start with only the public crime prompt, run read-only SQL against an in-memory copy of the game database, and submit suspects to the database's original solution checker. They stop successfully only after the checker confirms both stages.

| Script | API | Models |
| --- | --- | --- |
| `sql_mystery_agent.py` | OpenRouter Chat Completions | Tool-capable models from multiple providers |
| `sql_mystery_agent_openai.py` | OpenAI Responses | OpenAI GPT-5.6 models |

Both agents are cross-platform and use only Python's standard library. They require Python 3.8 or newer, internet access, an API key for the selected service, and API billing or credits.

At the end of every run, each agent prints benchmark metrics in the same format:

```text
Run metrics: 12 model turns, 2 failed solution submissions, 34.56 seconds total.
```

A model turn is one API response, including responses that request tools and the final-answer response. A failed solution submission is an incorrect suspect rejected by the game's solution trigger; malformed tool calls and database errors are not counted. Elapsed time measures the complete model/tool loop but excludes command startup and database loading.

### OpenRouter agent

Create an OpenRouter API key on the [OpenRouter Keys page](https://openrouter.ai/keys). The selected model must support tool calling; use OpenRouter's [tool-capable model filter](https://openrouter.ai/models?supported_parameters=tools) to find compatible model slugs.

In PowerShell:

```powershell
$env:OPENROUTER_API_KEY = "your-api-key"
py sql_mystery_agent.py
```

On macOS or Linux with Bash, Zsh, or a compatible shell:

```bash
export OPENROUTER_API_KEY="your-api-key"
python3 sql_mystery_agent.py
```

The OpenRouter agent supports these flags:

| Flag | Default | Description |
| --- | --- | --- |
| `--database PATH` | `sql-murder-mystery.db` next to the script | Use a different SQL Murder Mystery database file. |
| `--model MODEL` | `OPENROUTER_MODEL`, or `openrouter/auto-beta` when unset | Select an OpenRouter model slug. The auto router may choose any provider. |
| `--reasoning-effort LEVEL` | `medium` | Set reasoning effort to `none`, `minimal`, `low`, `medium`, `high`, or `xhigh`. OpenRouter maps the setting to models that use different reasoning controls. |
| `--max-tool-calls NUMBER` | `30` | Stop with an error if the agent exceeds this many database queries and solution submissions. |
| `-h`, `--help` | - | Display the command-line help. |

For example, explicitly test a Google model instead of using the auto router:

```powershell
py sql_mystery_agent.py `
  --model google/gemini-3-flash-preview `
  --reasoning-effort low
```

Use another provider by supplying any compatible OpenRouter model slug:

```powershell
py sql_mystery_agent.py `
  --model anthropic/claude-sonnet-4.5 `
  --reasoning-effort high
```

You can set the default model through the environment:

```powershell
$env:OPENROUTER_MODEL = "deepseek/deepseek-v3.2"
py sql_mystery_agent.py
```

For macOS or Linux, replace `py` with `python3`, replace PowerShell's line-continuation backticks with `\`, and use `export` to set environment variables.

### OpenAI agent

The earlier implementation remains available as `sql_mystery_agent_openai.py`. In PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
py sql_mystery_agent_openai.py
```

On macOS or Linux:

```bash
export OPENAI_API_KEY="your-api-key"
python3 sql_mystery_agent_openai.py
```

It supports the same `--database`, `--model`, and `--max-tool-calls` flags.
Its model defaults to `OPENAI_MODEL` or `gpt-5.6-sol`, and its `--reasoning-effort` choices are `none`, `low`, `medium`, `high`, `xhigh`, and `max`.

Display the flags for either implementation with:

```powershell
py sql_mystery_agent.py --help
py sql_mystery_agent_openai.py --help
```

### Agent tests

The local tests exercise the database safety checks and both provider-specific tool loops without making API calls or consuming credits.

In PowerShell:

```powershell
py -m unittest -v
```

On macOS or Linux:

```bash
python3 -m unittest -v
```


## Authors

* [Joon Park](https://twitter.com/JoonParkMusic)
* [Cathy He](https://twitter.com/Cathy_MeiyingHe)

## Inspiration
This murder mystery was inspired by [a crime in the neighboring Terminal City](https://github.com/veltman/clmystery "command-line murder mystery").

## Copyright and License
Original code for this project is released under [the MIT License](https://github.com/NUKnightLab/sql-mysteries/blob/master/LICENSE). 

Original text and other content is released under [Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). 

SQL query custom web components used here were adapted from code created and released to the public domain by Zi Chong Kao, creator of [Select Star SQL](https://selectstarsql.com/).

[Detective image by rambleron](https://www.vecteezy.com/vector-art/174092-clue-illustration) used under Vecteezy's free license.
