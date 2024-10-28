from flask import jsonify, request
from services.services import fetch_economy_data
from models.db_operations import fetch_country_data, store_country_data, get_economy_data
from utils.prompts import get_prompt_for_parameter, format_prompt, get_comprehensive_prompt
# import logging
from services.groq_service import generate_summary, get_country_data_summary


def setup_routes(app):
    @app.route('/country/<country_name>')
    def get_country_data_route(country_name):
        country_data = fetch_country_data(country_name)
        if country_data:
            return jsonify(country_data)
        else:
            # If not in database, try to fetch from API
            fetched_data = fetch_economy_data(country_name)
            if fetched_data:
                store_country_data(fetched_data)
                return jsonify(fetched_data)
            else:
                return jsonify({"error": "Country not found"}), 404

    @app.route('/fetch-and-store/<country_name>')
    def fetch_and_store_country(country_name):
        country_data = fetch_economy_data(country_name)
        if country_data:
            store_country_data(country_data)
            return jsonify({"message": f"Data for {country_name} fetched and stored successfully"})
        else:
            return jsonify({"error": "Failed to fetch country data"}), 404

    @app.route('/country-summary/<country_name>')
    def get_country_summary(country_name):
        country_data = fetch_country_data(country_name)
        if country_data:
            summary = get_country_data_summary(country_data)
            return jsonify(summary)
        else:
            return jsonify({"error": "Country not found"}), 404
        
    @app.route('/fetch-and-store-economy/<country_name>', methods=['GET', 'POST'])
    def fetch_and_store_economy(country_name):
        economy_data = fetch_economy_data(country_name)
        if economy_data:
            store_country_data(economy_data)
            return jsonify({"message": f"Economy data for {country_name} fetched and stored successfully", "data": economy_data})
        else:
            error_message = f"Failed to fetch economy data for {country_name}. Please check server logs for more details."
            # logger.error(error_message)
            return jsonify({"error": error_message}), 404

    @app.route('/economy/<country_name>')
    def get_economy_data_route(country_name):
        economy_data = get_economy_data(country_name)
        if economy_data:
            return jsonify(economy_data)
        else:
            return jsonify({"error": "Economy data not found"}), 404

    @app.route('/country-parameter-summary/<country_name>')
    def get_country_parameter_summary(country_name):
        parameter = request.args.get('parameter', '').lower()
        valid_parameters = ['population_density', 'trade', 'import_export']
        
        country_data = fetch_country_data(country_name)
        economy_data = get_economy_data(country_name)
        
        if not country_data and not economy_data:
            country_data = fetch_economy_data(country_name)
            if country_data:
                store_country_data(country_data)
        
        if not country_data and not economy_data:
            return jsonify({"error": "Country data not found"}), 404
        
        # Combine country_data and economy_data
        combined_data = {**country_data, **economy_data} if country_data and economy_data else country_data or economy_data or {}
        
        try:
            if parameter in valid_parameters:
                prompt = get_prompt_for_parameter(parameter)
            else:
                prompt = get_comprehensive_prompt()
            
            formatted_prompt = format_prompt(prompt, country_name, combined_data)
            summary = generate_summary(formatted_prompt)
            
            if summary:
                return jsonify({"summary": summary})
            else:
                return jsonify({"error": "Failed to generate summary"}), 500
        except Exception as e:
            # logger.error(f"Error processing request: {str(e)}")
            return jsonify({"error": f"Error processing request: {str(e)}"}), 500
