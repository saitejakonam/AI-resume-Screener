import React, { useState } from "react";
import axios from "axios";
import "./PageStyles.css";

const SearchCandidates = () => {
  const [filters, setFilters] = useState({ skills: "", experience: "", location: "" });
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const search = async () => {
    // Prevent empty search
    const hasInput = Object.values(filters).some((val) => val.trim() !== "");
    if (!hasInput) {
      setError("Please enter at least one search field.");
      setResults([]);
      return;
    }

    try {
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/resumes/search`, {
        params: filters,
      });

      const data = res.data?.results;
      if (Array.isArray(data)) {
        setResults(data);
        setError(null);
      } else {
        setResults([]);
        setError("No valid results returned.");
      }
    } catch (err) {
      console.error("Search error:", err);
      setError("Failed to fetch candidates. Try again later.");
      setResults([]);
    }
  };

  return (
    <div className="page-container">
      <h2>Search Candidates</h2>
      <div className="search-inputs">
        <input
          placeholder="Skills (e.g. Python)"
          value={filters.skills}
          onChange={(e) => setFilters({ ...filters, skills: e.target.value })}
        />
        <input
          placeholder="Experience"
          value={filters.experience}
          onChange={(e) => setFilters({ ...filters, experience: e.target.value })}
        />
        <input
          placeholder="Location"
          value={filters.location}
          onChange={(e) => setFilters({ ...filters, location: e.target.value })}
        />
        <button className="primary-btn" onClick={search}>
          Search
        </button>
      </div>

      {error && <p className="error-text">{error}</p>}

      <div className="search-results">
        {!error && results.length === 0 ? (
          <p className="no-data-text">No matching candidates found.</p>
        ) : (
          results.map((res, i) => (
            <div key={i} className="result-card">
              <h4>{res.data?.name || "Candidate"}</h4>
              <p><strong>Skills:</strong> {res.data?.skills || "N/A"}</p>
              <p><strong>Experience:</strong> {res.data?.experience || "N/A"}</p>
              <p><strong>Location:</strong> {res.data?.location || "N/A"}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SearchCandidates;
