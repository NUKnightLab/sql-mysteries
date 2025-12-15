-- sample_queries.sql
-- Purpose: Help beginners explore the SQL Mysteries database safely
-- These queries do NOT reveal the final solution

-- 1. View all tables in the database
SELECT name FROM sqlite_master WHERE type='table';

-- 2. Inspect the crime scene reports
SELECT *
FROM crime_scene_report
LIMIT 10;

-- 3. Find crimes that happened on a specific date
SELECT *
FROM crime_scene_report
WHERE date = 20180115;

-- 4. View people table structure
PRAGMA table_info(person);

-- 5. Find people by city
SELECT *
FROM person
WHERE city = 'SQL City'
LIMIT 10;

