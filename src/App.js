import "./App.css";
import React, { useState } from "react";
import Entry from "./Entry.js";
import { FaEnvelope, FaPhone, FaLinkedin, FaGithub } from "react-icons/fa";
import {
  SiPython, SiJavascript, SiTypescript, SiReact,
  SiPytorch, SiTensorflow, SiKeras, SiNumpy, SiPandas,
  SiPostgresql, SiGit, SiFigma, SiDocker
} from "react-icons/si";

function App() {
  // ===== 언어 토글 =====
  const [lang, setLang] = useState("KOR"); // 'KOR' | 'ENG'
  const t = {
    KOR: {
      headerTitle: "장우진 (Woojin) 포트폴리오",
      tagline: "LLM · RAG · 프론트엔드 — 정확도는 높이고, 지연·비용은 낮춥니다.",
      aboutTitle: "About",
      aboutText:
        "법률 RAG·멀티에이전트, React/Node 기반 UI/UX에 강점이 있습니다. 데이터로 문제를 정의하고 결과로 설득하는 개발자입니다.",
      projects: "프로젝트",
      mainProjects: "주요 프로젝트",
      otherProjects: "기타 프로젝트",
      achievements: "수상/성과",
      skills: "보유 기술",
      contact: "Contact",
      collapseUp: "▴",
      collapseDown: "▾",
    },
    ENG: {
      headerTitle: "Woojin (Jang Woojin) – Portfolio",
      tagline: "LLM · RAG · Frontend — Raise accuracy, lower latency & cost.",
      aboutTitle: "About",
      aboutText:
        "Strong in legal-domain RAG & multi-agent systems, plus React/Node UI/UX. I define problems with data and persuade with results.",
      projects: "Projects",
      mainProjects: "Main Projects",
      otherProjects: "Other Projects",
      achievements: "Achievements",
      skills: "Skills",
      contact: "Contact",
      collapseUp: "▴",
      collapseDown: "▾",
    },
  };

  // 펼침 상태
  const [expanded, setExpanded] = useState({
    projects: { expanded: true, entries: {} },
    achievements: { expanded: false, entries: {} },
    skills: { expanded: false },
  });

  const toggleSection = (sec) =>
    setExpanded((p) => ({ ...p, [sec]: { ...p[sec], expanded: !p[sec].expanded } }));

  const toggleEntry = (sec, key) =>
    setExpanded((p) => ({
      ...p,
      [sec]: {
        ...p[sec],
        entries: { ...p[sec].entries, [key]: !p[sec].entries[key] },
      },
    }));

  // ===== 프로젝트 데이터 (이미지/파일 없음: 안전) =====
  const lawI = {
    title: "[Law-I] AI 법률 비서 (RAG + Multi-Agent)",
    location: "Team project",
    dates: "2025.09 ~ 진행중",
    details: lang === "KOR"
      ? [
          "국가법령정보(법령·판례) 기반 RAG 파이프라인 설계: 청킹 → 임베딩(bge-m3) → FAISS/Chroma 검색.",
          "LangChain 기반 에이전트 오케스트레이션(Search/Drafting/Critic/Summary), '검색 없는 생성 금지' 가드레일.",
          "근거 카드(Evidence Pack)와 인용 자동화, FastAPI + AWS 배포.",
          "FE: React/Node, SPA 라우팅/검색/증거뷰 UI 제작."
        ]
      : [
          "RAG pipeline for Korean statutes/case law: chunking → embeddings (bge-m3) → FAISS/Chroma semantic search.",
          "LangChain agents (Search/Drafting/Critic/Summary) with 'no generation without retrieval' guardrails.",
          "Evidence pack + citation, FastAPI + AWS deployment.",
          "FE with React/Node: SPA routing, search UI, evidence viewer."
        ],
  };

  const santander = {
    title: "Kaggle – Santander Customer Transaction Prediction",
    location: "Kaggle",
    dates: "2025",
    details: lang === "KOR"
      ? [
          "Keras 이진분류 + 특성엔지니어링, 교차검증 설계.",
          "로컬 정확도 대비 리더보드 격차 분석 및 개선(시드/검증전략/앙상블)."
        ]
      : [
          "Keras binary classifier + feature engineering with K-Fold CV.",
          "Closed local-vs-LB gap via seeding/validation strategy/ensemble."
        ],
  };

  const quantum = {
    title: "Quantum AI – Fashion-MNIST 0↔6 분류",
    location: "AI Factory",
    dates: "2025",
    details: lang === "KOR"
      ? [
          "PennyLane 기반 QNN + CNN 하이브리드, Optuna 튜닝.",
          "엔드-투-엔드 제출 자동화 스크립트 구성."
        ]
      : [
          "PennyLane QNN + CNN hybrid with Optuna tuning.",
          "End-to-end submission automation pipeline."
        ],
  };

  const dacon = {
    title: "Dacon – 사이버공격 분류 / 신약개발 / 금융보안 LLM",
    location: "Dacon",
    dates: "2025",
    details: lang === "KOR"
      ? [
          "XGBoost/LightGBM/CatBoost 스태킹 앙상블, K-Fold + Optuna.",
          "RMSE/F1 지표 기반 피처·파이프라인 반복개선."
        ]
      : [
          "Stacked ensembles of XGB/LGBM/CatBoost with K-Fold + Optuna.",
          "Iterative feature/pipeline improvements on RMSE/F1."
        ],
  };

  // ===== 스킬 카드 =====
  const SkillItem = ({ Icon, label }) => (
    <div className="skill-item">
      <span className="skill-icon"><Icon size={18} /></span>
      <span className="skill-label">{label}</span>
    </div>
  );
  const SkillGroup = ({ title, items }) => (
    <div className="skill-card">
      <div className="skill-title">{title}</div>
      <div className="skill-items-wrap">
        {items.map((it, idx) => <SkillItem key={idx} Icon={it.Icon} label={it.label} />)}
      </div>
    </div>
  );

  const skillsData =
    lang === "KOR"
      ? [
          { title: "AI & 머신러닝", items: [
            { Icon: SiPytorch, label: "PyTorch" },
            { Icon: SiTensorflow, label: "TensorFlow" },
            { Icon: SiKeras, label: "Keras" },
            { Icon: SiNumpy, label: "NumPy" },
            { Icon: SiPandas, label: "Pandas" },
          ]},
          { title: "프론트엔드/언어", items: [
            { Icon: SiJavascript, label: "JavaScript" },
            { Icon: SiTypescript, label: "TypeScript" },
            { Icon: SiReact, label: "React" },
          ]},
          { title: "데이터/인프라", items: [
            { Icon: SiPostgresql, label: "PostgreSQL" },
            { Icon: SiDocker, label: "Docker" },
            { Icon: SiGit, label: "Git" },
            { Icon: SiFigma, label: "Figma" },
          ]},
        ]
      : [
          { title: "AI & ML", items: [
            { Icon: SiPytorch, label: "PyTorch" },
            { Icon: SiTensorflow, label: "TensorFlow" },
            { Icon: SiKeras, label: "Keras" },
            { Icon: SiNumpy, label: "NumPy" },
            { Icon: SiPandas, label: "Pandas" },
          ]},
          { title: "Frontend / Langs", items: [
            { Icon: SiJavascript, label: "JavaScript" },
            { Icon: SiTypescript, label: "TypeScript" },
            { Icon: SiReact, label: "React" },
          ]},
          { title: "Data / Infra", items: [
            { Icon: SiPostgresql, label: "PostgreSQL" },
            { Icon: SiDocker, label: "Docker" },
            { Icon: SiGit, label: "Git" },
            { Icon: SiFigma, label: "Figma" },
          ]},
        ];

  return (
    <div className="App">
      {/* 헤더 */}
      <header className="App-header">
        <h1>{t[lang].headerTitle}</h1>
        <p>{t[lang].tagline}</p>

        {/* 언어 토글 */}
        <div className="lang-toggle" aria-label="Language toggle" style={{ margin: "10px 0 16px" }}>
          <div
            className="lang-indicator"
            style={{ transform: `translateX(${lang === "ENG" ? "0" : "100%"})` }}
          />
          <button className={`lang-btn ${lang === "ENG" ? "active" : ""}`} onClick={() => setLang("ENG")}>
            ENG
          </button>
          <button className={`lang-btn ${lang === "KOR" ? "active" : ""}`} onClick={() => setLang("KOR")}>
            KOR
          </button>
        </div>

        {/* 연락처 */}
        <div className="contact-icons">
          <a href="mailto:wing0907@naver.com" aria-label="Email">
            <FaEnvelope size={28} style={{ margin: "0 12px", color: "#000" }} />
          </a>
          <a href="tel:+8210-0000-0000" aria-label="Phone">
            <FaPhone size={28} style={{ margin: "0 12px", color: "#000" }} />
          </a>
          <a href="https://github.com/wing0907" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
            <FaGithub size={28} style={{ margin: "0 12px", color: "#000" }} />
          </a>
          <a href="https://www.linkedin.com/in/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <FaLinkedin size={28} style={{ margin: "0 12px", color: "#000" }} />
          </a>
        </div>
      </header>

      {/* About */}
      <section className="About-section">
        <h2>{t[lang].aboutTitle}</h2>
        <p>{t[lang].aboutText}</p>
      </section>

      {/* Projects */}
      <section className="Project-section">
        <h2 onClick={() => toggleSection("projects")}>{t[lang].projects}</h2>
        {expanded.projects.expanded && (
          <div className="section-content">
            <h3 style={{ marginTop: 0 }}>{t[lang].mainProjects}</h3>

            <Entry
              title={lawI.title}
              location={lawI.location}
              dates={lawI.dates}
              details={lawI.details}
              isExpanded={expanded.projects.entries.lawI}
              onClick={() => toggleEntry("projects", "lawI")}
            />
            <Entry
              title={santander.title}
              location={santander.location}
              dates={santander.dates}
              details={santander.details}
              isExpanded={expanded.projects.entries.santander}
              onClick={() => toggleEntry("projects", "santander")}
            />
            <Entry
              title={quantum.title}
              location={quantum.location}
              dates={quantum.dates}
              details={quantum.details}
              isExpanded={expanded.projects.entries.quantum}
              onClick={() => toggleEntry("projects", "quantum")}
            />
            <Entry
              title={dacon.title}
              location={dacon.location}
              dates={dacon.dates}
              details={dacon.details}
              isExpanded={expanded.projects.entries.dacon}
              onClick={() => toggleEntry("projects", "dacon")}
            />
          </div>
        )}
      </section>

      {/* Achievements (원하면 채워넣기) */}
      <section className="Achievements-section">
        <h2 onClick={() => toggleSection("achievements")}>{t[lang].achievements}</h2>
        {expanded.achievements.expanded && (
          <div className="section-content">
            <Entry
              title={lang === "KOR" ? "퀀텀 AI 해커톤 우수상" : "Quantum AI Hackathon – Excellence Prize"}
              location="AI Factory"
              dates="2025"
              details={
                lang === "KOR"
                  ? ["패션-MNIST 양자과제 본선, 우수상 수상."]
                  : ["Finalist; Excellence Prize for quantum AI application."]
              }
              isExpanded={expanded.achievements.entries.qai}
              onClick={() => toggleEntry("achievements", "qai")}
            />
          </div>
        )}
      </section>

      {/* Skills */}
      <section className="Skills-section">
        <h2 onClick={() => toggleSection("skills")}>{t[lang].skills}</h2>
        {expanded.skills.expanded && (
          <div className="section-content">
            <div className="skills-grid">
              {skillsData.map((g, i) => (
                <SkillGroup key={i} title={g.title} items={g.items} />
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Contact footer */}
      <section className="Contact-section">
        <h2>{t[lang].contact}</h2>
        <p>
          Email: <a href="mailto:wjj9319@gmail.com">wing0907@naver.com</a> · GitHub:{" "}
          <a href="https://github.com/wing0907" target="_blank" rel="noreferrer">github.com/wing0907</a>
        </p>
        <footer>© {new Date().getFullYear()} Woojin</footer>
      </section>
    </div>
  );
}

export default App;
