import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import CreateJob from "./pages/CreateJob";
import ViewJobs from "./pages/ViewJobs";
import ApplyResume from "./pages/ApplyResume";
import RankedResumes from "./pages/RankedResumes";
import SearchCandidates from "./pages/SearchCandidates";
import ViewResume from "./pages/ViewResume";
const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create-job" element={<CreateJob />} />
        <Route path="/view-jobs" element={<ViewJobs />} />
        <Route path="/apply/:jobId" element={<ApplyResume />} />
        <Route path="/ranked/:jobId" element={<RankedResumes />} />
        <Route path="/search" element={<SearchCandidates />} />
        <Route path="/resume/:candidateId" element={<ViewResume />} />
      </Routes>
    </>
  );
};

export default App;
