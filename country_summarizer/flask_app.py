import os
from dotenv import load_dotenv
import requests
import psycopg2
from flask import Flask, jsonify, request
from groq import Groq


# Load environment variables
load_dotenv()

# Flask application setup
app = Flask(__name__)

# Your API key
API_KEY = os.getenv('YOUR_API_KEY')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

groq_client = Groq(api_key=GROQ_API_KEY)

# Database connection function
def get_db_connection():
    try:
        connection = psycopg2.connect( 
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# PART-1: Make a request and print the response
def fetch_country_data(country_name):
    api_url = f"https://api.api-ninjas.com/v1/country?name={country_name}"
    try:
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()[0]
        print("API Response:", data)  # Print the response
        return {
            'name': country_name,
            'surface_area': data['surface_area'],
            'exports': data.get('exports', 0),
            'tourists': data.get('tourists', 0),
            'gdp': data['gdp'],
            'population': data['population']
        }
    except requests.RequestException as e:
        print(f"Error fetching country data: {e}")
        return None

# PART-2: Store data in the database
def setup_database():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE,
            surface_area FLOAT,
            exports FLOAT,
            tourists INTEGER,
            gdp FLOAT,
            population INTEGER
        );
        """)
        
        conn.commit()
    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def store_country_data(data):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO countries (name, surface_area, exports, tourists, gdp, population)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE SET
            surface_area = EXCLUDED.surface_area,
            exports = EXCLUDED.exports,
            tourists = EXCLUDED.tourists,
            gdp = EXCLUDED.gdp,
            population = EXCLUDED.population;
        """
        
        cursor.execute(insert_query, (
            data['name'], data['surface_area'], data['exports'],
            data['tourists'], data['gdp'], data['population']
        ))
        
        conn.commit()
    except Exception as e:
        print(f"Error storing country data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

# PART-3: API to retrieve data from the database
@app.route('/country/<country_name>')
def get_country_data(country_name):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM countries WHERE name = %s", (country_name,))
        country_data = cursor.fetchone()
        
        if country_data:
            return jsonify({
                "name": country_data[1],
                "surface_area": country_data[2],
                "exports": country_data[3],
                "tourists": country_data[4],
                "gdp": country_data[5],
                "population": country_data[6]
            })
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        print(f"Error retrieving country data: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# To fetch and store the data in the db
@app.route('/fetch-and-store/<country_name>')
def fetch_and_store_country(country_name):
    country_data = fetch_country_data(country_name)
    if country_data:
        store_country_data(country_data)
        return jsonify({"message": f"Data for {country_name} fetched and stored successfully"})
    else:
        return jsonify({"error": "Failed to fetch country data"}), 404

# PART-4: API to generate a simple summary
@app.route('/country-summary/<country_name>')
def get_country_summary(country_name):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM countries WHERE name = %s", (country_name,))
        country_data = cursor.fetchone()
        
        if not country_data:
            return jsonify({"error": "Country not found"}), 404
        
        country_info = {
            "name": country_data[1],
            "surface_area": country_data[2],
            "exports": country_data[3],
            "tourists": country_data[4],
            "gdp": country_data[5],
            "population": country_data[6]
        }
        
        prompt = f"""Generate a concise summary for {country_info['name']} based on the following data:
        Surface Area: {country_info['surface_area']} sq km
        Exports: ${country_info['exports']} billion
        Annual Tourists: {country_info['tourists']} million
        GDP: ${country_info['gdp']} billion
        Population: {country_info['population']}

        Provide insights on the country's economy, tourism, and demographics in a paragraph."""

        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise country summaries based on provided data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            max_tokens=200,
            temperature=0.7
        )

        summary = response.choices[0].message.content.strip()

        return jsonify({"country": country_name, "summary": summary})
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return jsonify({"error": "Failed to generate summary"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
