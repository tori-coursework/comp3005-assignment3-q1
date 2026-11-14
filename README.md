# COMP 3005 – Assignment 3 Q1: Students CRUD App

A python app that connects to a PostgreSQL and performs CRUD operations on a `students` table.

## Structure
```
database/
    01_create_database.sql    creates students_db
    02_schema_and_data.sql    creates students table + initial data
app/
    students_app.py           The application
    requirements.txt         
```

## Setup
0. Requires PostgreSQL installed and running. Tested on PSQL 18 on Windows.
1. **Create the database:** in pgAdmin, open the Query Tool on `postgres` and run `database/01_new_database.sql`.
2. **Create the table and initial data:** open the Query Tool on `students_db` and run `database/02_create_and_insert_data.sql`.
3. **Install the dependency (psycopg2-binary):**
   ```
   pip install -r app/requirements.txt
   ```

## Run
```
python app/students_app.py
```
Enter your PostgreSQL password when prompted, then choose the 5 options from the menu.

