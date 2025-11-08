import "./App.css";
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PortfolioPage from "./components/PortfolioPage";
import { portfolioData } from "./data/portfolioData";

const NotFound = () => (
  <div className="not-found">
    <h1>404</h1>
    <p>Page not found.</p>
    <div className="not-found-links">
      <a href="/ko">한국어 페이지로 이동</a>
      <a href="/en">Go to English page</a>
    </div>
  </div>
);

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/ko" replace />} />
        <Route path="/ko" element={<PortfolioPage data={portfolioData.ko} />} />
        <Route path="/en" element={<PortfolioPage data={portfolioData.en} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
