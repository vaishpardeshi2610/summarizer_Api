# Country Economic Data API

This project is a Flask-based API that fetches, stores, and summarizes economic data for various countries. It uses external APIs for data retrieval and the Groq API for generating summaries.

## Features

- Fetch and store country economic data
- Generate summaries of country economic data
- Retrieve stored country data
- Custom parameter-based summaries

## Prerequisites

- Python 3.7+
- pip
- PostgreSQL database

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/country-economic-data-api.git
   cd country-economic-data-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   DATABASE_URL=postgresql://username:password@localhost/dbname
   API_NINJAS_KEY=your_api_ninjas_key
   GROQ_API_KEY=your_groq_api_key
   ```

5. Set up the database:
   ```
   python models/db_config.py
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /country/<country_name>`: Retrieve stored data for a specific country
- `GET /fetch-and-store/<country_name>`: Fetch and store data for a specific country
- `GET /country-summary/<country_name>`: Get a summary of a country's economic data
- `GET /country-parameter-summary/<country_name>`: Get a parameter-specific summary of a country's economic data

## Project Structure
country-economic-data-api/
│
├── app.py
├── routes/
│ ├── init.py
│ └── endpoints.py
├── services/
│ ├── init.py
│ └── country_data_service.py
├── models/
│ ├── init.py
│ └── db_config.py
├── .env
├── requirements.txt
└── README.md

