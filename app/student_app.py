import sys, psycopg2
from datetime import date
from getpass import getpass

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
        
def main():
    conn = get_connection()
    print("Now connected to PostgreSQL.")

if __name__ == "__main__":
    main()