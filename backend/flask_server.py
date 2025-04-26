from flask import Flask, jsonify, request
import subprocess
import json
import os
import logging
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# In development, allow all origins
CORS(app)

# For production, use this instead:
# CORS(app, resources={r"/scrape": {"origins": "http://yourfrontendurl.com"}})

@app.route('/scrape', methods=['GET'])
def scrape():
    logger.info("Scrape request received")
    
    # Relative path to the Scrapy project
    scrapy_project_path = os.path.join(os.path.dirname(__file__), 'researchscraper')
    output_file = os.path.join(scrapy_project_path, 'output.json')
    
    # Remove old output file if it exists
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            logger.info("Removed old output file")
        except Exception as e:
            logger.error(f"Failed to remove old output file: {e}")
    
    try:
        # Run the Scrapy spider
        logger.info("Starting Scrapy spider")
        result = subprocess.run(
            ['scrapy', 'crawl', 'research', '-o', 'output.json'],
            cwd=scrapy_project_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Scrapy process failed: {result.stderr}")
            return jsonify({'error': result.stderr}), 500
        
        # Check if output file was created
        if not os.path.exists(output_file):
            logger.error("Output file not found after scraping")
            return jsonify({'error': 'Output file not found after scraping.'}), 500
        
        # Parse the JSON data
        try:
            with open(output_file) as f:
                data = json.load(f)
                logger.info(f"Successfully scraped {len(data)} research items")
            return jsonify(data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return jsonify({'error': f'Failed to decode JSON: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)