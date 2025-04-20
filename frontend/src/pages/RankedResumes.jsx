import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getRankedResumes } from "../utils/api";
import "./PageStyles.css";

const RankedResumes = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [ranked, setRanked] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRanked = async () => {
      try {
        const res = await getRankedResumes(jobId);
        if (Array.isArray(res.ranked_candidates)) {
          const maxScore = Math.max(...res.ranked_candidates.map((r) => r.score || 0));

          const withPercentiles = res.ranked_candidates.map((item) => ({
            ...item,
            percentile: maxScore > 0 ? ((item.score / maxScore) * 100).toFixed(2) : "0.00"
          }));

          setRanked(withPercentiles);
        } else {
          setRanked([]);
        }
        setError(null);
      } catch (err) {
        console.error("Error fetching ranked resumes:", err);
        setError("Failed to fetch ranked resumes. Try again later.");
        setRanked([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRanked();
  }, [jobId]);

  return (
    <div className="page-container">
      <h2 className="page-title">Ranked Resumes for Job #{jobId}</h2>

      {loading ? (
        <p className="loading-text">Loading ranked resumes...</p>
      ) : error ? (
        <p className="error-text">{error}</p>
      ) : ranked.length === 0 ? (
        <p className="no-data-text">No resumes ranked yet for this job.</p>
      ) : (
        <div className="ranked-results">
          {ranked.map((item, index) => (
            <div className="resume-card" key={item.candidate_id?.toString() || index}>
              <h3 className="resume-rank">#{index + 1}</h3>
              <p><strong>Name:</strong> {item.data?.name || "N/A"}</p>
              <p><strong>Email:</strong> {item.data?.email || "N/A"}</p>
              <p><strong>Skills:</strong> {item.data?.skills || "N/A"}</p>
              <p><strong>Experience:</strong> {item.data?.experience || "N/A"}</p>
              <p><strong>Location:</strong> {item.data?.location || "N/A"}</p>
              <p><strong>Score:</strong> {item.score ? item.score.toFixed(2) : "N/A"}</p>
              <p><strong>Relevance:</strong> {item.percentile}%</p>

              <button
                className="primary-btn"
                onClick={() => navigate(`/resume/${item.candidate_id}`)}
              >
                View Resume
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RankedResumes;
