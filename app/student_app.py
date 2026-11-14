import sys, psycopg2
from datetime import date
from getpass import getpass
from psycopg2 import errors

# Global defaults for postgresql
HOST = "localhost"
PORT = 5432
NAME = "students_db"
USER = "postgres"


# Function to open a connection to the PostgreSQL database, password is asked at startup
def get_connection():
    password = getpass("PostgreSQL password: ")

    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            dbname=NAME,
            user=USER,
            password=password,
        )
        return conn
    except psycopg2.OperationalError as error:
        print(f"Could not connect to the database:\n{error}")
        sys.exit(1)
        
"""
Function to ask for a text input from the user
Returns the text value if valid, otherwise prompts again.
"""
def ask_for_text(prompt):
    while True:
        textvalue = input(prompt).strip()
        
        if textvalue:
            return textvalue
        print("Please enter a value.")
        
"""
Function to ask for a integer input from the user
Returns the integer value if valid, otherwise prompts again.
"""
def ask_for_int(prompt):
    while True:
        textvalue = input(prompt).strip()
        
        if textvalue.isdigit():
            return int(textvalue)
        print("Please enter a valid integer.")
        
"""
Function to ask for a date input from the user using the format YYYY-MM-DD. 
Returns None if the user enters nothing.
"""
def ask_for_date(prompt):
    while True:
        textvalue = input(prompt).strip()
        
        if not textvalue:
            return None
        
        try:
            year, month, day = map(int, textvalue.split("-"))
            return date(year, month, day)
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")

"""
Function to retrieve all students from the connected psql database.
A cursor is used to execute the SQL query and fetch all rows from the students table. 
The results are printed in a formatted table.
Returns None if no students are found.
"""
def getAllStudents(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students ORDER BY student_id;")
        rows = cur.fetchall()

    if not rows:
        print("No student data found.")
        return

    print(f"{'ID':<6} {'First':<10} {'Last':<10} {'Email':<28} Enrolled")
    
    for studid, first, last, email, enrolled in rows:
        print(f"{studid:<6} {first:<10} {last:<10} {email:<28} {enrolled or '-'}")
        
"""
Function to add a new student to the connected psql database. 
A cursor is used to execute the SQL query and insert the new student into the students table.
The function takes the first name, last name, email, and enrollment date as parameters.
"""
def addStudent(conn, first_name, last_name, email, enrollment_date):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id;",
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
            
        conn.commit()
        print(f"Added student with ID {new_id}.")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"The email '{email}' already exists.")
        
"""
Function to update a student's email in the connected psql database given student ID and new email.
A cursor is used to execute the SQL query and update a pre-existing student's email in the students table.
The function prints a message indicating whether the update was successful or not.
"""
def updateStudentEmail(conn, student_id, new_email):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )
            updated = cur.rowcount
            
        conn.commit()
        
        if updated == 0:
            print(f"No student with ID {student_id}.")
            
        else:
            print(f"Updated student {student_id} email to {new_email}.")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"The email '{new_email}' already exists. Use a different one")
        
"""
Function to delete a student from the connected psql database given student ID.
A cursor is used to execute the SQL query and delete the student from the students table.
The function prints a message indicating whether the deletion was successful.
"""
def deleteStudent(conn, student_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        deleted = cur.rowcount
    conn.commit()

    if deleted == 0:
        print(f"No student with ID {student_id}.")
    else:
        print(f"Deleted student {student_id}.")
        
def main():
    conn = get_connection()
    print("Now connected to PostgreSQL.\n")
    
    try:
        while True:
            print("1. Show all students")
            print("2. Add a student")
            print("3. Update a student email")
            print("4. Delete a student")
            print("0. Exit the Program")
            choice = input("Choose: ").strip()

            if choice == "1":
                getAllStudents(conn)
            elif choice == "2":
                first = ask_for_text("First name: ")
                last = ask_for_text("Last name: ")
                email = ask_for_text("Email: ")
                enrolled = ask_for_date("Enrollment date (YYYY-MM-DD, leave blank for none): ")
                addStudent(conn, first, last, email, enrolled)
            elif choice == "3":
                student_id = ask_for_int("Student ID to update: ")
                new_email = ask_for_text("New email: ")
                updateStudentEmail(conn, student_id, new_email)
            elif choice == "4":
                student_id = ask_for_int("Student ID to delete: ")
                deleteStudent(conn, student_id)
            else:
                print("Invalid option.")
    finally:
        conn.close()



if __name__ == "__main__":
    main()