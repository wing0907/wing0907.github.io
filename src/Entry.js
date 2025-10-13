// src/Entry.js
import React from "react";

export default function Entry({
  title,
  location,
  dates,
  details = [],
  isExpanded = false,
  onClick = () => {},
}) {
  return (
    <article>
      <div className="entry-header" onClick={onClick}>
        <div>
          <h3 className="entry-title">{title}</h3>
          {(location || dates) && (
            <p className="entry-meta">
              {location}
              {location && dates ? " · " : ""}
              {dates}
            </p>
          )}
        </div>
        <span className={`arrow ${isExpanded ? "expanded" : ""}`}>▾</span>
      </div>

      {isExpanded && (
        <div className="entry-details">
          {Array.isArray(details) ? (
            <ul>
              {details.map((d, i) => (
                <li key={i}>{d}</li>
              ))}
            </ul>
          ) : (
            details
          )}
        </div>
      )}
    </article>
  );
}
