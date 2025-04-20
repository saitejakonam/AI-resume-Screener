import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "./PageStyles.css";

const ApplyResume = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [files, setFiles] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      alert("Please select at least one file.");
      return;
    }

    const formData = new FormData();
    for (let file of files) {
      formData.append("files", file);
    }

    setLoading(true);
    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/resumes/upload/${jobId}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (res.status === 200 || res.status === 201) {
        alert("Resumes uploaded and ranked successfully!");
        navigate(`/ranked/${jobId}`);
      } else {
        alert("Upload completed but server did not return success status.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to upload resumes. Check API status or browser console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="upload-card">
        <h2>Upload Resumes for Job #{jobId}</h2>
        <p>Select PDF or DOCX Resumes:</p>
        <input
          type="file"
          multiple
          onChange={(e) => setFiles(e.target.files)}
        />
        <button className="primary-btn" onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload & Rank Resumes"}
        </button>
      </div>
    </div>
  );
};

export default ApplyResume;
