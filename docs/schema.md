\# SQL Mysteries – Database Schema



This document describes the tables used in the SQL Mysteries database.

It is intended to help beginners understand the structure before

writing queries.



---



\## crime\_scene\_report

Stores reports filed by police officers.



\*\*Columns:\*\*

\- `date` – Date of the crime

\- `type` – Type of crime

\- `description` – Detailed report text

\- `city` – City where the crime occurred



---



\## person

Contains personal details of people in the database.



\*\*Columns:\*\*

\- `id` – Unique person ID

\- `name` – Full name

\- `license\_id` – Driver license ID

\- `address\_number` – House number

\- `address\_street\_name` – Street name

\- `ssn` – Social security number



---



\## interview

Stores interview transcripts.



\*\*Columns:\*\*

\- `person\_id` – References `person.id`

\- `transcript` – Interview text



---



\## drivers\_license

Driver license information.



\*\*Columns:\*\*

\- `id` – License ID

\- `age` – Age of license holder

\- `height` – Height

\- `eye\_color` – Eye color

\- `hair\_color` – Hair color

\- `gender` – Gender

\- `plate\_number` – Vehicle plate



