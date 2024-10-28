from models.db_config import get_db_connection

def fetch_country_data(country_name):
    """Fetches country data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM country_economy WHERE country_name = %s", (country_name,))
    country_data = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if country_data:
        return {
            "country_name": country_data[0],
            "surface_area": country_data[1],
            "exports": country_data[2],
            "tourists": country_data[3],
            "gdp": country_data[4],
            "population": country_data[5],
            "imports": country_data[6],
            "urban_population_growth": country_data[7],
            "urban_population": country_data[8],
            "gdp_growth": country_data[9],
            "gdp_per_capita": country_data[10]
        }
    return None

def store_country_data(data):
    """Stores country data in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO country_economy (
        country_name, surface_area, exports, tourists, gdp, population,
        imports, urban_population_growth, urban_population, gdp_growth, gdp_per_capita
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (country_name) DO UPDATE SET
        surface_area = EXCLUDED.surface_area,
        exports = EXCLUDED.exports,
        tourists = EXCLUDED.tourists,
        gdp = EXCLUDED.gdp,
        population = EXCLUDED.population,
        imports = EXCLUDED.imports,
        urban_population_growth = EXCLUDED.urban_population_growth,
        urban_population = EXCLUDED.urban_population,
        gdp_growth = EXCLUDED.gdp_growth,
        gdp_per_capita = EXCLUDED.gdp_per_capita;
    """
    
    try:
        cursor.execute(insert_query, (
            data['country_name'],
            float(data.get('surface_area', 0)),
            float(data.get('exports', 0)),
            float(data.get('tourists', 0)),
            float(data.get('gdp', 0)),
            int(data.get('population', 0)),
            float(data.get('imports', 0)),
            float(data.get('urban_population_growth', 0)),
            int(data.get('urban_population', 0)),
            float(data.get('gdp_growth', 0)),
            float(data.get('gdp_per_capita', 0))
        ))
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_economy_data(country_name):
    """Retrieves economy data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM country_economy WHERE country_name = %s", (country_name,))
    economy_data = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if economy_data:
        return {
            "country_name": economy_data[0],
            "imports": economy_data[1],
            "urban_population_growth": economy_data[2],
            "exports": economy_data[3],
            "population": economy_data[4],
            "urban_population": economy_data[5],
            "gdp": economy_data[6],
            "gdp_growth": economy_data[7],
            "gdp_per_capita": economy_data[8],
            "surface_area": economy_data[9] if len(economy_data) > 9 else 0
        }
    return None

