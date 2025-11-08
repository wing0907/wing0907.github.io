import React from "react";
import { Link } from "react-router-dom";
import { FaExternalLinkAlt } from "react-icons/fa";

const PortfolioPage = ({ data }) => {
  const { locale, hero, sections, footerNote } = data;
  const switchPath = locale === "ko" ? "/en" : "/ko";
  const switchLabel = locale === "ko" ? "View English Page" : "한국어 페이지 보기";

  const renderSectionContent = (section) => {
    switch (section.layout) {
      case "bullets":
        return (
          <ul className="bullet-list">
            {section.items.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        );
      case "columns":
        return (
          <div className="columns-grid">
            {section.columns.map((col, idx) => (
              <div className="column-card" key={idx}>
                <h3>{col.title}</h3>
                <ul>
                  {col.items.map((item, itemIdx) => (
                    <li key={itemIdx}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        );
      case "stack":
        return (
          <div className="stack-list">
            {section.items.map((item, idx) => (
              <article className="stack-card" key={idx}>
                <header>
                  <div className="stack-card-heading">
                    <h3>{item.title}</h3>
                    {item.subtitle && <p className="stack-subtitle">{item.subtitle}</p>}
                  </div>
                  {(item.period || item.location) && (
                    <div className="stack-meta">
                      {item.period && <span className="stack-period">{item.period}</span>}
                      {item.location && <span className="stack-location">{item.location}</span>}
                    </div>
                  )}
                </header>
                {item.bullets && (
                  <ul className="stack-bullets">
                    {item.bullets.map((line, bulletIdx) => (
                      <li key={bulletIdx}>{line}</li>
                    ))}
                  </ul>
                )}
                {item.tags && (
                  <div className="tag-list">
                    {item.tags.map((tag, tagIdx) => (
                      <span className="tag-chip" key={tagIdx}>
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
                {item.links && renderLinks(item.links)}
              </article>
            ))}
          </div>
        );
      case "grid":
        return (
          <div className="grid-cards">
            {section.items.map((item, idx) => (
              <article className="info-card" key={idx}>
                <header>
                  <h3>{item.title}</h3>
                  {item.highlight && <p className="info-highlight">{item.highlight}</p>}
                  {item.period && <p className="info-period">{item.period}</p>}
                </header>
                {item.bullets && (
                  <ul className="info-list">
                    {item.bullets.map((line, bulletIdx) => (
                      <li key={bulletIdx}>{line}</li>
                    ))}
                  </ul>
                )}
                {item.links && renderLinks(item.links)}
              </article>
            ))}
          </div>
        );
      case "cards":
        return (
          <div className="card-grid">
            {section.items.map((item, idx) => (
              <article className="info-card" key={idx}>
                <header>
                  <h3>{item.title}</h3>
                  {item.highlight && <p className="info-highlight">{item.highlight}</p>}
                  {item.period && <p className="info-period">{item.period}</p>}
                </header>
                {item.bullets && (
                  <ul className="info-list">
                    {item.bullets.map((line, bulletIdx) => (
                      <li key={bulletIdx}>{line}</li>
                    ))}
                  </ul>
                )}
                {item.links && renderLinks(item.links)}
              </article>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  const renderLinks = (links) => (
    <div className="link-list">
      {links.map((link, idx) => {
        const isMail = link.href?.startsWith("mailto:");
        const linkProps = isMail
          ? {}
          : { target: "_blank", rel: "noopener noreferrer" };
        return (
          <div className="link-item" key={idx}>
            <a href={link.href} {...linkProps}>
              <span>{link.label}</span>
              {!isMail && <FaExternalLinkAlt aria-hidden="true" />}
            </a>
            {link.note && <p className="link-note">{link.note}</p>}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className={`portfolio-page locale-${locale}`}>
      <div className="language-switcher">
        <Link to={switchPath}>{switchLabel}</Link>
      </div>

      <header className="hero">
        <div className="hero-content">
          <p className="hero-tagline">{hero.tagline}</p>
          <h1>{hero.name}</h1>
          <h2>{hero.title}</h2>
          <p className="hero-summary">{hero.summary}</p>

          {hero.highlights?.length > 0 && (
            <div className="hero-highlights">
              {hero.highlights.map((item, idx) => (
                <span className="hero-chip" key={idx}>
                  {item}
                </span>
              ))}
            </div>
          )}

          {hero.stats?.length > 0 && (
            <div className="hero-stats">
              {hero.stats.map((stat, idx) => (
                <div className="hero-stat-card" key={idx}>
                  <div className="hero-stat-value">{stat.value}</div>
                  <div className="hero-stat-label">{stat.label}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <aside className="hero-aside">
          <div className="hero-aside-card">
            <h3>{locale === "ko" ? "연락처 & 정보" : "Contact & Facts"}</h3>
            <ul className="fact-list">
              {hero.quickFacts.map((fact, idx) => (
                <li key={idx}>
                  <span className="fact-label">{fact.label}</span>
                  {fact.href ? (
                    <a
                      href={fact.href}
                      target={fact.href.startsWith("http") ? "_blank" : undefined}
                      rel={fact.href.startsWith("http") ? "noopener noreferrer" : undefined}
                    >
                      {fact.value}
                    </a>
                  ) : (
                    <span className="fact-value">{fact.value}</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </aside>
      </header>

      <main>
        {sections.map((section) => (
          <section className="portfolio-section" id={section.id} key={section.id}>
            <div className="section-header">
              <h2>{section.title}</h2>
              {section.subtitle && <p className="section-subtitle">{section.subtitle}</p>}
            </div>
            {renderSectionContent(section)}
          </section>
        ))}
      </main>

      {footerNote && <footer className="portfolio-footer">{footerNote}</footer>}
    </div>
  );
};

export default PortfolioPage;
