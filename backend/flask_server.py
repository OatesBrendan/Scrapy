from flask import Flask, jsonify
import subprocess
import json
import os
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['GET'])
def scrape():
    # Relative path to the Scrapy project
    scrapy_project_path = os.path.join(os.path.dirname(__file__), 'researchscraper')

    output_file = os.path.join(scrapy_project_path, 'output.json')

    result = subprocess.run(
        ['scrapy', 'crawl', 'research', '-o', 'output.json'],
        cwd=scrapy_project_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({'error': result.stderr}), 500

    if not os.path.exists(output_file):
        return jsonify({'error': 'Output file not found.'}), 500

    try:
        with open(output_file) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to decode JSON: {str(e)}'}), 500

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
