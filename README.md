# Research Scraper Application

A web application that scrapes research publications and displays them in a table.

## Project Structure
```
research-scraper/
├── backend/                # Flask and Scrapy backend
│   ├── flask_server.py     # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── researchscraper/    # Scrapy project
│       └── ...
└── research-app/           # React frontend
    ├── src/                # React source code
    ├── package.json        # Node.js dependencies
    └── ...
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```
   python flask_server.py
   ```
   The API will be available at http://localhost:5000

### Frontend Setup
1. Install Node.js dependencies:
   ```
   cd research-app
   npm install
   ```

2. Start the React development server:
   ```
   npm start
   ```
   The application will be available at http://localhost:3000

## Usage
1. Open the web app in your browser
2. Click the "Fetch Research Data" button
3. View the scraped research data in the table