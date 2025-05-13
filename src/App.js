// src/App.js
import "./App.css";
import React, { useState, useRef } from "react";
import Entry from "./Entry";
import { FaEnvelope, FaPhone, FaLinkedin, FaGithub } from "react-icons/fa";
import {
  SiPython, SiTensorflow, SiPytorch, SiNumpy, SiPandas,
  SiJavascript, SiTypescript, SiReact,
  SiPostgresql, SiDocker, SiGit, SiFigma
} from "react-icons/si";

/** 프로필 이미지: public/profile.jpg 가 있으면 노출, 없으면 자동 숨김 */
function ProfileAvatar() {
  const imgRef = useRef(null);
  return (
    <img
      ref={imgRef}
      src="/profile.jpg"
      alt="Profile"
      onError={() => imgRef.current && (imgRef.current.style.display = "none")}
      style={{
        width: 108, height: 108, borderRadius: "50%",
        objectFit: "cover", border: "1px solid #e5e7eb"
      }}
    />
  );
}

export default function App() {
  // ===== 언어 토글 =====
  const [lang, setLang] = useState("KOR"); // 'KOR' | 'ENG'
  const t = {
    KOR: {
      name: "장우진",
      title: "AI/풀스택 엔지니어",
      tagline: "LLM · RAG · React — 정확도는 높이고, 지연/비용은 낮춥니다.",
      aboutTitle: "About",
      aboutText:
        "법률 도메인 RAG·멀티 에이전트와 React 기반 제품 개발에 강점이 있습니다. 데이터로 문제를 정의하고 결과로 설득하는 개발자입니다.",
      experience: "경력",
      projects: "프로젝트",
      achievements: "수상/성과",
      skills: "보유 기술",
      contact: "Contact",
      mainProjects: "주요 프로젝트",
      collapseUp: "▴",
      collapseDown: "▾",
    },
    ENG: {
      name: "Woojin Jang",
      title: "AI / Full-Stack Engineer",
      tagline: "LLM · RAG · React — Raise accuracy, lower latency & cost.",
      aboutTitle: "About",
      aboutText:
        "Strong in legal-domain RAG & multi-agent systems and React-based product development. I define problems with data and persuade with results.",
      experience: "Experience",
      projects: "Projects",
      achievements: "Achievements",
      skills: "Skills",
      contact: "Contact",
      mainProjects: "Main Projects",
      collapseUp: "▴",
      collapseDown: "▾",
    },
  };

  // 섹션 펼침 상태
  const [expanded, setExpanded] = useState({
    experience: { expanded: true, entries: {} },
    projects: { expanded: true, entries: {} },
    achievements: { expanded: true, entries: {} },
    skills: { expanded: false },
  });
  const toggleSection = (sec) =>
    setExpanded((p) => ({ ...p, [sec]: { ...p[sec], expanded: !p[sec].expanded } }));
  const toggleEntry = (sec, key) =>
    setExpanded((p) => ({
      ...p,
      [sec]: { ...p[sec], entries: { ...p[sec].entries, [key]: !p[sec].entries[key] } },
    }));

  /* =========================
     데이터 (이미지/파일 의존성 없음)
     ========================= */

  // --- 경력
  const exp_ibm = {
    title:
      lang === "KOR"
        ? "[IBM x RedHat] AI Transformation – 수강생(6개월)"
        : "[IBM x RedHat] AI Transformation – Trainee (6 months)",
    location: lang === "KOR" ? "대한민국 (온/오프라인)" : "Korea (hybrid)",
    dates:
      lang === "KOR"
        ? "2025.05.13 ~ 현재"
        : "May 13, 2025 – Present",
    details:
      lang === "KOR"
        ? [
            "LLM·RAG, 프롬프트 엔지니어링·에이전트 오케스트레이션 심화.",
            "TensorFlow/PyTorch로 DNN·CNN·RNN·NLP 실습, 실전 과제 수행.",
            "FastAPI·Docker·AWS로 서빙/배포 파이프라인 경험.",
          ]
        : [
            "Deep dive into LLM/RAG, prompt engineering, and agent orchestration.",
            "Hands-on DNN/CNN/RNN/NLP with TensorFlow/PyTorch.",
            "FastAPI/Docker/AWS for serving & deployment.",
          ],
  };

  // --- 프로젝트
  const pj_lawI = {
    title: lang === "KOR" ? "[Law-I] AI 법률 비서 (RAG + Multi-Agent)" : "[Law-I] Legal AI Assistant (RAG + Multi-Agent)",
    location: "Side / Team",
    dates: lang === "KOR" ? "2025 ~ 진행중" : "2025 – Ongoing",
    details:
      lang === "KOR"
        ? [
            "국가법령·판례 기반 RAG: 청킹 → 임베딩(bge-m3) → FAISS/Chroma.",
            "LangChain 에이전트(Search/Draft/Critic) + ‘검색 없는 생성 금지’ 가드레일.",
            "증거팩/인용 자동화, React UI, FastAPI + AWS 배포.",
          ]
        : [
            "RAG on statutes/caselaw: chunking → embeddings (bge-m3) → FAISS/Chroma.",
            "LangChain agents (Search/Draft/Critic) with guardrails.",
            "Evidence pack & citations, React UI, FastAPI + AWS.",
          ],
  };

  // --- 수상
  const awd_quantum = {
    title:
      lang === "KOR"
        ? "제1회 퀀텀AI 경진대회 우수상 (전주대학교 총장상)"
        : "1st Quantum AI Competition – Excellence Prize (President of Jeonju Univ.)",
    location: lang === "KOR" ? "Norma & AI Factory 주최" : "Hosted by Norma & AI Factory",
    dates: "2025",
    details:
      lang === "KOR"
        ? [
            "Fashion-MNIST 양자 분류 과제 해결(QNN + CNN 하이브리드).",
            "Optuna로 하이퍼파라미터 튜닝, 제출 파이프라인 자동화.",
          ]
        : [
            "Solved Fashion-MNIST quantum task (QNN + CNN hybrid).",
            "Optuna tuning, automated submission pipeline.",
          ],
  };

  // --- 스킬
  const skills =
    lang === "KOR"
      ? [
          { title: "AI/ML", items: [
            { Icon: SiPython, label: "Python" },
            { Icon: SiTensorflow, label: "TensorFlow" },
            { Icon: SiPytorch, label: "PyTorch" },
            { Icon: SiNumpy, label: "NumPy" },
            { Icon: SiPandas, label: "Pandas" },
          ]},
          { title: "프론트엔드", items: [
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
          { title: "AI/ML", items: [
            { Icon: SiPython, label: "Python" },
            { Icon: SiTensorflow, label: "TensorFlow" },
            { Icon: SiPytorch, label: "PyTorch" },
            { Icon: SiNumpy, label: "NumPy" },
            { Icon: SiPandas, label: "Pandas" },
          ]},
          { title: "Frontend", items: [
            { Icon: SiJavascript, label: "JavaScript" },
            { Icon: SiTypescript, label: "TypeScript" },
            { Icon: SiReact, label: "React" },
          ]},
          { title: "Data/Infra", items: [
            { Icon: SiPostgresql, label: "PostgreSQL" },
            { Icon: SiDocker, label: "Docker" },
            { Icon: SiGit, label: "Git" },
            { Icon: SiFigma, label: "Figma" },
          ]},
        ];

  // ===== UI =====
  return (
    <div className="App">
      {/* 헤더 */}
      <header className="App-header">
        <div style={{ display:"flex", alignItems:"center", gap:16 }}>
          <ProfileAvatar />
          <div>
            <h1 style={{ margin:0 }}>{t[lang].name}</h1>
            <div style={{ color:"#64748b", marginTop:2 }}>{t[lang].title}</div>
          </div>
        </div>
        <p style={{ marginTop:12 }}>{t[lang].tagline}</p>

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
            <FaEnvelope size={28} style={{ margin: "0 12px" }} />
          </a>
          <a href="tel:+8210-0000-0000" aria-label="Phone">
            <FaPhone size={28} style={{ margin: "0 12px" }} />
          </a>
          <a href="https://github.com/wing0907" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
            <FaGithub size={28} style={{ margin: "0 12px" }} />
          </a>
          <a href="https://www.linkedin.com/in/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <FaLinkedin size={28} style={{ margin: "0 12px" }} />
          </a>
        </div>
      </header>

      {/* About */}
      <section className="About-section">
        <h2>{t[lang].aboutTitle}</h2>
        <p>{t[lang].aboutText}</p>
      </section>

      {/* Experience */}
      <section className="Experience-section">
        <h2 onClick={() => toggleSection("experience")}>{t[lang].experience}</h2>
        {expanded.experience.expanded && (
          <div className="section-content">
            <Entry
              title={exp_ibm.title}
              location={exp_ibm.location}
              dates={exp_ibm.dates}
              details={exp_ibm.details}
              isExpanded={expanded.experience.entries.ibm}
              onClick={() => toggleEntry("experience", "ibm")}
            />
          </div>
        )}
      </section>

      {/* Projects */}
      <section className="Project-section">
        <h2 onClick={() => toggleSection("projects")}>{t[lang].projects}</h2>
        {expanded.projects.expanded && (
          <div className="section-content">
            <h3 style={{ marginTop: 0 }}>{t[lang].mainProjects}</h3>
            <Entry
              title={pj_lawI.title}
              location={pj_lawI.location}
              dates={pj_lawI.dates}
              details={pj_lawI.details}
              isExpanded={expanded.projects.entries.lawI}
              onClick={() => toggleEntry("projects", "lawI")}
            />
          </div>
        )}
      </section>

      {/* Achievements */}
      <section className="Achievements-section">
        <h2 onClick={() => toggleSection("achievements")}>{t[lang].achievements}</h2>
        {expanded.achievements.expanded && (
          <div className="section-content">
            <Entry
              title={awd_quantum.title}
              location={awd_quantum.location}
              dates={awd_quantum.dates}
              details={awd_quantum.details}
              isExpanded={expanded.achievements.entries.quantum}
              onClick={() => toggleEntry("achievements", "quantum")}
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
              {skills.map((g, i) => (
                <div className="skill-card" key={i}>
                  <div className="skill-title">{g.title}</div>
                  <div className="skill-items-wrap">
                    {g.items.map((it, idx) => (
                      <div className="skill-item" key={idx}>
                        <span className="skill-icon"><it.Icon size={18} /></span>
                        <span className="skill-label">{it.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Contact */}
      <section className="Contact-section">
        <h2>{t[lang].contact}</h2>
        <p>
          Email: <a className="App-link" href="mailto:wing0907@naver.com">wing0907@naver.com</a> · GitHub:{" "}
          <a className="App-link" href="https://github.com/wing0907" target="_blank" rel="noreferrer">github.com/wing0907</a>
        </p>
        <footer>© {new Date().getFullYear()} {t[lang].name}</footer>
      </section>
    </div>
  );
}
