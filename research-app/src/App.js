import React, { useState } from 'react';
import axios from 'axios';

function ResearchTable() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/scrape');
      setData(response.data);
    } catch (error) {
      console.error('Scraping failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button className="btn btn-primary" onClick={handleScrape} disabled={loading}>
        {loading ? 'Scraping...' : 'Fetch Research Data'}
      </button>
      {data.length > 0 && (
        <table className="table mt-3">
          <thead>
            <tr>
              <th>Year</th>
              <th>Title</th>
              <th>Authors</th>
              <th>URL</th>
            </tr>
          </thead>
          <tbody>
            {data.map((entry, idx) => (
              <tr key={idx}>
                <td>{entry.year}</td>
                <td>{entry.title}</td>
                <td>{entry.authors.join(', ')}</td>
                <td><a href={entry.url} target="_blank" rel="noopener noreferrer">Link</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ResearchTable;
