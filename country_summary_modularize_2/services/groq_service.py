import os
from groq import Groq
import logging
from utils.prompts import COUNTRY_SUMMARY_PROMPT

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=GROQ_API_KEY)

def get_country_data_summary(country_data):
    """Generates a summary for the specified country."""
    if not country_data:
        return None

    prompt = COUNTRY_SUMMARY_PROMPT.format(
        country_name=country_data['country_name'],
        surface_area=country_data['surface_area'],
        exports=country_data['exports'],
        tourists=country_data.get('tourists', 'N/A'),
        gdp=country_data['gdp'],
        population=country_data['population']
    )

    try:
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
            model="mixtral-8x7b-32768",  # Updated model name
            max_tokens=200
        )

        summary = response.choices[0].message.content.strip()
        return {"country": country_data['country_name'], "summary": summary}
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return None

def generate_summary(prompt):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise summaries based on economic data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",  # Updated model name
            max_tokens=500,
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return None
