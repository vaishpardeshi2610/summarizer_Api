import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    try:
        connection = psycopg2.connect( #it is a python drive for postgres
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        return connection
    except Exception as e:
        return None

def setup_database():
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()  #a cursor object is an interface to execute SQL commands and retrieve data from a database. It allows the program to execute queries, fetch data, and navigate through records one by one or in batches.
    
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS country_economy (
            country_name VARCHAR(255) PRIMARY KEY,
            surface_area FLOAT,
            exports FLOAT,
            tourists FLOAT,
            gdp FLOAT,
            population BIGINT,
            imports FLOAT,
            urban_population_growth FLOAT,
            urban_population BIGINT,
            gdp_growth FLOAT,
            gdp_per_capita FLOAT
        );
        """)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_database()
