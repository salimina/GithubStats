import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 

const App = () => {
  const [username, setUsername] = useState('');
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isEmpty, setIsEmpty] = useState(false);

  const handleFetchStats = async () => {
    setIsLoading(true);
    setError(null);
    setIsEmpty(false);

    try {
      const response = await axios.get(`http://localhost:5000/api/user-stats/${username}`);
      const data = response.data;
      
      if (data.totalRepos === 0) {
        setIsEmpty(true);
      } else {
        setStats(data);
      }

      setError(null);
    } catch (err) {
      setError('Failed to fetch data');
      setStats(null);
    }

    setIsLoading(false);
  };

  return (
    <div className="container">
      <div className="spline-background">
        <iframe
          title="Spline 3D"
          src="https://my.spline.design/particlenebula-05a6a2ae15444d5b1ad7b29202713277/"
          frameBorder="0"
          width="100%"
          height="100%"
        ></iframe>
      </div>
      <div className="content">
        <h1>GitHub User Statistics</h1>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter GitHub username"
        />
        <button onClick={handleFetchStats}>Fetch Stats</button>

        {isLoading && <p className="loading">Loading...</p>}
        {error && <p className="error">{error}</p>}
        {isEmpty && <p className="empty">No repositories found for this user.</p>}

        {stats && !isEmpty && (
          <div className="stats">
            <h2>Statistics for {username}</h2>
            <p>Total Repositories: {stats.totalRepos}</p>
            <p>Total Forks: {stats.totalForks}</p>
            <p>Total Stargazers: {stats.totalStargazers}</p>
            <h3>Languages Used:</h3>
            <ul>
              {Array.isArray(stats.languages) && stats.languages.length > 0 ? (
                stats.languages.map(([language, count]) => (
                  <li key={language}>{language}: {count}</li>
                ))
              ) : (
                <li>No languages data available</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;

