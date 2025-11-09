import "./App.css";
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PortfolioPage from "./components/PortfolioPage";
import { portfolioData } from "./data/portfolioData";

const getBasename = (publicUrl) => {
  if (!publicUrl || publicUrl === ".") {
    return "/";
  }

  try {
    const { pathname } = new URL(publicUrl);
    if (!pathname || pathname === "/") {
      return "/";
    }
    return pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
  } catch (err) {
    if (publicUrl.startsWith("/")) {
      return publicUrl.endsWith("/") && publicUrl !== "/"
        ? publicUrl.slice(0, -1)
        : publicUrl;
    }

    const normalized = `/${publicUrl}`.replace(/\/+$/, "");
    return normalized === "" ? "/" : normalized;
  }
};

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
  const basename = React.useMemo(() => getBasename(process.env.PUBLIC_URL), []);

  return (
    <BrowserRouter basename={basename}>
      <Routes>
        <Route path="/" element={<Navigate to="/ko" replace />} />
        <Route path="/ko" element={<PortfolioPage data={portfolioData.ko} />} />
        <Route path="/en" element={<PortfolioPage data={portfolioData.en} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
