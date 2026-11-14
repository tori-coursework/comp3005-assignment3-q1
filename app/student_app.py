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
        
def deleteStudent(conn, student_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        deleted = cur.rowcount
    conn.commit()

    if deleted == 0:
        print(f"[ERROR] No student with ID {student_id}.")
    else:
        print(f"Deleted student {student_id}.")
        
def main():
    conn = get_connection()
    print("Now connected to PostgreSQL.")

if __name__ == "__main__":
    main()