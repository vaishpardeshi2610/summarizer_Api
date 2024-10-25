# Economic Data Summary Generator

This application fetches economic data for countries and generates summaries based on specific economic parameters using AI.

## Application Flow

1. **API Endpoint**: 
   The main endpoint is `/country-parameter-summary/<country_name>?parameter=<parameter>`.

2. **Parameter Validation**:
   - Valid parameters are 'population_density', 'trade', and 'import_export'.
   - If an invalid parameter is provided, the application returns an error.

3. **Data Retrieval**:
   - The application first attempts to retrieve economic data for the specified country from the local database.
   - If the data is not found in the database, it fetches the data from an external API (API Ninjas).
   - Newly fetched data is stored in the database for future use.

4. **Prompt Generation**:
   - Based on the specified parameter, a relevant prompt is selected from predefined templates in `prompts.py`.
   - The prompt is then formatted with the retrieved economic data.

5. **Summary Generation**:
   - The formatted prompt is sent to the Groq AI model.
   - Groq generates a concise summary based on the economic data and the specific parameter.

6. **Response**:
   - The application returns the generated summary as a JSON response.

## Key Components

- `routes.py`: Contains the main route handler and orchestrates the flow of the application.
- `services.py`: Handles data retrieval from the database and external API.
- `prompts.py`: Contains prompt templates and formatting functions for different economic parameters.
- Database: Stores economic data for countries to reduce API calls.
- Groq AI: Used for generating summaries based on the economic data and prompts.

## Setup and Running

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `YOUR_API_KEY`: Your API Ninjas key
3. Set up the PostgreSQL database and update connection details in `config.py`.
4. Run the Flask application: `python app.py`

## API Usage

Send a GET request to:
http://localhost:5000/country-parameter-summary/<country_name>?parameter=<parameter>

Example: http://localhost:5000/country-parameter-summary/India?parameter=trade

Response:
{
  "summary": "India has a robust economy with a GDP of $2779352 billion, making it one of the world's leading economies. Its GDP growth rate stands at an impressive 6.80%, significantly outpacing the global average (3.6%) and the regional average (5.2%) for 2021. This above-average growth rate indicates a strong momentum in India's economic expansion, fueling its future prospects.\n\nHowever, India's GDP per capita is relatively low at $2054.8, which is considerably lesser than the global average ($11,355.5) and regional average ($5,513.3). This relatively low per capita income, despite the large overall GDP, suggests that the wealth is not evenly distributed among the population. It also implies that India is still in the process of development, with a need for continued focus on poverty alleviation and equitable distribution of resources.\n\nThe trade-to-GDP ratio of 28.86% indicates that international trade plays a moderate role in India's economy. Increasing this ratio could help spur economic growth further, but it would require addressing factors that may be hindering robust trade growth, such as infrastructure challenges and bureaucratic barriers.\n\nAnalyzing the factors that contribute to or hinder India's economic growth, the"
}


2. For a comprehensive summary of all parameters:
   Send a GET request to:
   ```
   http://localhost:5000/country-parameter-summary/<country_name>
   ```
   Example:
   ```
   http://localhost:5000/country-parameter-summary/India


   Response:
   {
      "summary": "Austria displays a solid overall economic health with a GDP of $455508 billion, growing at a rate of 2.40%, and a GDP per capita of $51230.3, reflecting decent living standards. Urbanization is still in its infancy, with only 0.66% of the 9 million inhabitants living in urban areas, and a slow urban population growth rate of 0.70%. This low population density and urbanization leave vast room for spatial development, potential urbanization, and corresponding infrastructure investments.\n\nAustria's trade profile indicates significant international economic integration, with a trade to GDP ratio of 76.43%. Exports and imports both account for about one-third of the GDP, creating a moderate trade deficit of $5064 billion. Such a high trade openness index implies that Austria is susceptible to global economic fluctuations. Nevertheless, it also opens opportunities for specialization, technological exchange, and growth through international trade.\n\nThe Austrian economy boasts key strengths in its robust GDP growth, high GDP per capita, and significant trade volume. However, challenges arise from the trade deficit and high dependency on international trade, which could be affected by protectionist measures or global economic downturns. Moreover, low urbanization and population density may result in inefficient infrastructure and service distribution, leading to increased costs and reduced competitiveness.\n\nTo strengthen the economy, Austria could focus on policies that foster innovation, technological advancement, and export promotion. Furthermore, policies that encourage urbanization, targeted infrastructure development, and sustainable spatial planning can improve efficiency and competitiveness. Addressing the trade deficit by fostering export-oriented sectors while carefully managing import growth could further bolster Austria's economic resilience and long-term growth prospects."
   }

   ```

The response will be a JSON object containing the generated summary.

## Error Handling

The application includes error handling for:
- Invalid parameters
- Missing country data
- AI model errors
- Database errors

In case of any errors, appropriate error messages are returned in the API response.