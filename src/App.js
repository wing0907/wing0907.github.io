// import logo from './logo.svg';
import './App.css';
import Mybutton from './components/Buttons.js'
import React, { useState } from 'react';
import Entry from './Entry';
import degreeImage from './assets/images/graduation.jpg';
import judoImage1 from './assets/images/judo1.jpg';
import judoImage2 from './assets/images/judo2.jpg';
import judoImage3 from './assets/images/judo3.jpg';
import dissImage from './assets/images/dissertationlogo.jpg';
import cotonsImage1 from './assets/images/cotons1.jpg';
import cotonsImage2 from './assets/images/cotons2.jpg';
import favaImage1 from './assets/images/fava1.jpeg';
import favaImage2 from './assets/images/fava2.jpeg';
import cesImage1 from './assets/images/ces1.jpeg';
import cesImage2 from './assets/images/ces2.jpeg';
import cesImage3 from './assets/images/ces3.jpeg';
import jagriImage1 from './assets/images/jagri1.jpeg';
import jagriImage2 from './assets/images/jagri2.jpeg';
import edisonImage from './assets/images/edison1.jpeg';
import senseoneImage1 from './assets/images/senseone1.png';
import senseoneImage2 from './assets/images/senseone2.png';
import senseoneImage3 from './assets/images/senseone3.png';
import senseoneImage4 from './assets/images/senseone4.png';
import senseoneImage5 from './assets/images/senseone5.png';
import royalUrImage1 from './assets/images/royalur1.png';
import royalUrImage2 from './assets/images/royalur2.png';
import sudokuImage1 from './assets/images/sudoku1.png';
import sudokuImage2 from './assets/images/sudoku2.png';
import sudokuImage3 from './assets/images/sudoku3.png';
import sudokuImage4 from './assets/images/sudoku4.png';
import sudokuImage5 from './assets/images/sudoku5.png';
import auraIdIamge1 from './assets/images/auraid1.png';
import auraIdIamge2 from './assets/images/auraid2.png';
import auraIdIamge3 from './assets/images/auraid3.png';
import auraIdIamge4 from './assets/images/auraid4.png';
import auraIdIamge5 from './assets/images/auraid5.png';
import auraIdIamge6 from './assets/images/auraid6.png';
import auraIdIamge7 from './assets/images/auraid7.png';
import elizaImage1 from './assets/images/eliza1.png';
import elizaImage2 from './assets/images/eliza2.png';
import elizaImage3 from './assets/images/eliza3.png';
import quantumImage1 from './assets/images/quantum1.jpeg';
import quantumImage2 from './assets/images/quantum2.jpeg';
import quantumImage3 from './assets/images/quantum3.jpeg';
import quantumImage4 from './assets/images/quantum4.jpeg';
import daconImage1 from './assets/images/dacon1.png';
import daconImage2 from './assets/images/dacon2.png';
import daconImage3 from './assets/images/dacon3.png';
import daconImage4 from './assets/images/dacon4.png';
import daconImage5 from './assets/images/dacon5.png';
import hackathon1 from './assets/images/hackathon1.png';
import hackathon2 from './assets/images/hackathon2.png';
import hackathon3 from './assets/images/hackathon3.png';
import hackathon4 from './assets/images/hackathon4.png';
import hackathon5 from './assets/images/hackathon5.png';
import ibmImage1 from './assets/images/ibmImage1.png';
import dissertation1 from './assets/files/CSDissertation.pdf';
import dissertation2 from './assets/files/MathDissertation.pdf';
import dissertationImage1 from './assets/images/dissertation1.png';
import dissertationImage2 from './assets/images/dissertation2.png';
import productionapk from './assets/files/cotons-production-gateway.apk';
import { FaEnvelope, FaPhone, FaLinkedin, FaGithub } from 'react-icons/fa';

// ===== 스킬 아이콘 =====
import {
  SiPython, SiJavascript, SiTypescript, SiKotlin, SiDart,
  SiReact, SiFlutter,
  SiPytorch, SiTensorflow, SiKeras, SiNumpy, SiPandas,
  SiMysql, SiMongodb, SiPostgresql,
  SiGit, SiJira, SiConfluence, SiSlack,
  SiFigma, SiAdobeillustrator, SiOpenai, SiDocker
} from 'react-icons/si';

import { FaJava } from 'react-icons/fa';

function App() {

  // ===== 언어 상태 & 라벨 i18n =====
  const [lang, setLang] = useState('ENG'); // 'ENG' | 'KOR'
  const t = {
    ENG: {
      headerTitle: "Jae Woo Chang's Portfolio",
      work: "Work Experience",
      engagements: "Professional Engagements",
      projects: "Project Engagements",
      otherProjects: "Other Projects",
      achievements: "Achievements / Awards",
      education: "Education/Qualification",
      skills: "Skills",
      companyAbout: "What Company is CareSix?",
      futureOfVet: "Future Of Veterinary Care",
      companyMore: "More about the company",
      officialSite: "official website",
      downloadApk: "Download app APK",
      mainProjects: "Main Projects",
      collapseUp: "▴",
      collapseDown: "▾",
    },
    KOR: {
      headerTitle: "장재우 포트폴리오",
      work: "경력",
      engagements: "대외활동",
      projects: "프로젝트",
      otherProjects: "기타 프로젝트",
      achievements: "수상 / 성과",
      education: "학력/자격",
      skills: "보유기술",
      companyAbout: "CareSix는 어떤 회사?",
      futureOfVet: "수의학의 미래",
      companyMore: "회사 더보기",
      officialSite: "공식 웹사이트",
      downloadApk: "앱 APK 다운로드",
      mainProjects: "주요 프로젝트",
      collapseUp: "▴",
      collapseDown: "▾",
    }
  };

  // 공통: 언어별 텍스트 배열에 공통 미디어 노드를 덧붙여 주는 헬퍼
  const getDetails = (engTexts, korTexts, mediaNode) => {
    const withMedia = mediaNode ? (arr) => [...arr, mediaNode] : (arr) => arr;
    return lang === 'ENG' ? withMedia(engTexts) : withMedia(korTexts);
  };

  const [expandedSections, setExpandedSections] = useState({
    experience: {expanded: false, entries: {}},
    education: {expanded: false, entries: {}},
    skills: {expanded:false},
    volunteer: {expanded:false},
    caresixContent: {expanded:false},
    engagements: {expanded: false, entries: {}},
    projects: {expanded: false, entries: {}},
    achievements: {expanded: false, entries: {}},
  });

  const toggleSection = (section) => {
    setExpandedSections((prevState) => ({
      ...prevState,
      [section]: {
        ...prevState[section],
        expanded: !prevState[section].expanded,
      },
    }));
  };

  const toggleEntry = (section, entry) => {
    setExpandedSections((prevState) => ({
      ...prevState,
      [section]: {
        ...prevState[section],
        entries: {
          ...prevState[section].entries,
          [entry]: !prevState[section].entries[entry],
        },
      },
    }));
  };

  // ====== Work ======
  const work_ai_title = lang === 'ENG' ? "AI/ML Engineer & Researcher, CareSix Co., LTD" : "AI/ML 엔지니어 & 리서처, 케어식스";
  const work_ai_details_ENG = [
    'Developed a machine learning-based algorithm for canine heart rate estimation using Long Short-Term Memory (LSTM) models with TensorFlow and Keras.',
    'Designed an AI-driven system for detecting IJK peaks in ballistocardiogram (BCG) signals, leveraging deep learning-based signal processing.',
    'Applied unsupervised learning techniques to automate IJK peak detection, reducing dependency on ECG signals.',
    'Incorporated mathematical modeling of physiological signals to extract domain-specific features, capturing the periodicity of IJK peaks.',
    'Enhanced preprocessing pipeline by applying advanced noise reduction techniques, improving signal-to-noise ratio and robustness of model input features.'
  ];
  const work_ai_details_KOR = [
    'TensorFlow/Keras 기반 LSTM으로 개 심박 추정 알고리즘을 개발.',
    'BCG 신호의 IJK 피크를 딥러닝 신호처리로 검출하는 AI 시스템 설계.',
    'ECG 의존도를 낮추기 위해 IJK 피크 비지도 검출 적용.',
    '생체신호의 주기성(IJK)을 수학적 모델링으로 도메인 특화 피처로 반영.',
    '고급 노이즈 제거로 전처리 강화(SNR 향상, 입력 피처 견고성 개선).'
  ];

  const work_web_title = lang === 'ENG' ? "Web Developer, CareSix Co., LTD" : "웹 개발자, 케어식스";
  const work_web_details_ENG = [
    'Developed a web-based dog recognition platform using TypeScript with React, integrating a backend algorithm for dog identification.',
    'Designed and built a hospital management system for veterinary hospitals and pet tracking.',
    'Integrated AWS RDS for secure data management and scalability.',
  ];
  const work_web_details_KOR = [
    'TypeScript/React 기반 반려견 인식 웹 플랫폼 개발(백엔드 알고리즘 연동).',
    '수의 병원용 관리 시스템(환자/케이지 기록 추적) 설계·구현.',
    'AWS RDS 연동으로 보안·확장성 보장.',
  ];

  const work_app_title = lang === 'ENG' ? "App Developer, CareSix Co., LTD" : "앱 개발자, 케어식스";
  const work_app_details_ENG = [
    <div key="detail-1">
      Developed a production-grade application in Kotlin for the Sense1 Vet model, actively used in the device manufacturing and deployment process. 
      The app automated mapping of NFC tags, QR codes, and barcodes into a structured CSV format, ensuring traceability and quality control. -
      <a href={productionapk} download style={{ marginLeft: '8px', textDecoration: 'underline', color: '#007BFF' }}>
        {t[lang].downloadApk}
      </a>
    </div>,
    'Built a Bluetooth-enabled app (Cotons AI) in Flutter for capturing BCG signals, 6-axis sensor data, and temperature readings.',
  ];
  const work_app_details_KOR = [
    <div key="detail-1">
      Kotlin으로 Sense1 Vet 양산/배포 공정에 실제 사용되는 프로덕션급 앱을 개발. 
      NFC/QR/바코드 매핑을 자동화하여 CSV로 내보내고, 추적 가능성과 품질 관리를 보장. -
      <a href={productionapk} download style={{ marginLeft: '8px', textDecoration: 'underline', color: '#007BFF' }}>
        {t[lang].downloadApk}
      </a>
    </div>,
    'Flutter(블루투스 연동)로 BCG/6축 센서/온도 데이터 수집 앱(Cotons AI) 개발.',
  ];

  const work_math_title = lang === 'ENG' ? "Mathematician, CareSix Co., LTD" : "수학 리서처, 케어식스";
  const work_math_details_ENG = [
    'Implemented Fourier Transform in Python to filter noise from BCG measurements, enhancing signal clarity.',
    'Conducted statistical analysis using Python and NumPy to validate algorithm effectiveness.',
  ];
  const work_math_details_KOR = [
    'Python 기반 푸리에 변환으로 BCG 노이즈 제거, 신호 명료도 향상.',
    'Python/NumPy 통계 분석으로 알고리즘 효과 검증.',
  ];

  // Company info
  const company_awards_list_ENG = ['CES Best Tech Innovation Award 2022', 'Edison Awards Nominee 2024'];
  const company_awards_list_KOR = ['CES Best Tech Innovation Award 2022', 'Edison Awards 후보 2024'];
  const company_awards_media = (
    <div 
      key="awards-images" 
      style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}
    >
      <img src={cotonsImage2} alt="CES Awards" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={edisonImage} alt="Edison Awards" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );

  // ===== Engagements =====
  const jAgri_media = (
    <div key="jagri-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={jagriImage1} alt="J-Agri Exhibition 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={jagriImage2} alt="J-Agri Exhibition 2" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const jAgri_ENG = [
    'Represented HRG as Lead Manager, showcasing the 2025 CES Innovation Awards-winning project: the first-ever wearable cow health monitor.',
    'Engaged with industry leaders, shared insights, and connected with experts in agricultural technology.',
    'Demonstrated innovative approaches to livestock health monitoring, receiving significant industry recognition.',
  ];
  const jAgri_KOR = [
    'HRG 리드 매니저로 참가, 2025 CES 혁신상 수상 프로젝트(세계 최초 착용형 소 헬스 모니터) 전시.',
    '애그테크 업계 리더들과 네트워킹 및 기술 인사이트 공유.',
    '가축 헬스 모니터링의 혁신적 접근 시연, 업계 주목.',
  ];

  const fava_media = (
    <div key="fava-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={favaImage1} alt="Fava Exhibition 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={favaImage2} alt="Fava Exhibition 2" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const fava_ENG = [
    'Represented CareSix, connecting with veterinary professionals and industry innovators across Asia.',
    'Showcased award-winning devices, including the Sense1 Pro dog wearable and the Sense1 Guardian, both receiving positive feedback from doctors and professionals.',
    'Engaged in discussions about advancing veterinary technology and animal healthcare solutions.',
  ];
  const fava_KOR = [
    'CareSix 대표로 참가, 아시아 수의사/업계 혁신가들과 교류.',
    'Sense1 Pro/Guardian 등 수상 디바이스 전시, 의료진으로부터 긍정적 피드백 확보.',
    '수의 테크와 동물 헬스케어 솔루션 발전에 대한 논의 참여.',
  ];

  const ces_media = (
    <div key="ces2025-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={cesImage1} alt="CES 2025 Exhibition 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={cesImage2} alt="CES 2025 Exhibition 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={cesImage3} alt="CES 2025 Exhibition 3" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const ces_ENG = [
    'Invited to exhibit at CES 2025 in Venetian Suite 29-225.',
    'Showcasing the latest advancements in veterinary technology and wearable animal health monitoring devices.',
    'Networking with global tech leaders and innovators to push the boundaries of animal healthcare solutions.',
  ];
  const ces_KOR = [
    'CES 2025 Venetian Suite 29-225 전시 초청.',
    '수의 테크/웨어러블 헬스 모니터링 최신 기술 시연.',
    '글로벌 테크 리더들과 네트워킹을 통해 헬스케어 한계 확장.',
  ];

  // --- Hackathon section (updated) ---
  const hackathon_media = (
    <div key="hackathon-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={hackathon1} alt="K-Digital Training AI Hackathon" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={hackathon2} alt="K-Digital Training AI Hackathon" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={hackathon3} alt="K-Digital Training AI Hackathon" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={hackathon4} alt="K-Digital Training AI Hackathon" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={hackathon5} alt="K-Digital Training AI Hackathon" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );

  const hackathon_ENG = [
    "K-Digital Training AI Hackathon – built a reckless-driving detection system (dashcam video).",
    "Used YOLOv8 (Ultralytics) with custom weight training; post-processing tracked object trajectories to classify behaviors.",
    "Behaviors detected: aggressive cut-in (unsafe lane insertion), hard braking/deceleration, overspeeding, etc.",
    "Mobile app flow: plate number, location, and offense type are auto-filled from inference; user adds details and submits a report.",
    "Advanced to the finals (finalist), eliminated in the grand final.",
  ];

  const hackathon_KOR = [
    "K-디지털 트레이닝 AI 해커톤 – 대시캠 영상 기반 ‘난폭운전 감지 시스템’ 개발.",
    "YOLOv8(Ultralytics) 모델 가중치 학습 후, 후처리에서 트래킹 궤적·속도·가감속 특성으로 행위 분류.",
    "탐지 항목: 무리한 끼어들기, 급정지/급제동, 과속 등 난폭운전 유형.",
    "앱 연동: 차량번호·위치·위반유형을 자동 추출해 포맷에 채워주고, 사용자가 상세 입력 후 신고 제출 가능.",
    "본선 진출, 결선 탈락.",
  ];

  // ===== Projects – Main =====
  const sense1_media = (
    <div key="sense1vet-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={senseoneImage1} alt="SenseOne Project 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={senseoneImage2} alt="SenseOne Project 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={senseoneImage3} alt="SenseOne Project 3" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={senseoneImage4} alt="SenseOne Project 4" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={senseoneImage5} alt="SenseOne Project 5" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );

  
  const pj_sense1_ENG = [
    'Developed a machine learning-based AI algorithm for canine heart rate estimation using Long Short-Term Memory (LSTM) models.',
    'Designed and implemented signal processing techniques to analyze ballistocardiogram (BCG) data for heart rate detection.',
    'Applied Python-based Fourier Transform and Wavelet Decomposition to remove noise and extract meaningful heart-rate frequency components from raw BCG signals.',
    'Verified algorithm performance improvement through statistical analysis using Python and NumPy.',
    'Built a deep learning pipeline using TensorFlow and Keras to enhance real-time heart rate monitoring accuracy.',
    'Applied unsupervised learning for IJK peak detection, reducing dependency on ECG signals for heart rate analysis.',
    'Incorporated mathematical modeling of physiological signals to extract domain-specific features, capturing the periodicity of IJK peaks.',
    'Enhanced preprocessing pipeline by applying advanced noise reduction techniques, improving signal-to-noise ratio and robustness of model input features.',
    'Improved heart rate measurement accuracy from unstable readings caused by canine trembling or motion to 96% accuracy after applying the AI algorithm.',
    'Collaborated with hardware engineers and production teams to optimize data acquisition and improve signal quality.',
    'Contributed to the development of Sense1 Vet, an AI-powered wearable device for veterinary health monitoring.',
  ];
  const pj_sense1_KOR = [
    'TensorFlow/Keras LSTM으로 개 심박 추정 AI 알고리즘을 개발.',
    'BCG 데이터의 심박 검출을 위한 신호처리 기법을 설계 및 구현.',
    'Python 기반 푸리에 변환과 웨이블릿 변환으로 원시 신호의 노이즈를 제거하고 의미 있는 심박 주파수 성분을 추출.',
    'Python과 NumPy를 활용한 통계 분석으로 알고리즘 성능 개선 효과를 검증.',
    '실시간 심박 모니터링 정확도 향상을 위한 딥러닝 파이프라인을 구축.',
    'ECG 의존도를 줄이기 위해 IJK 피크 비지도 검출 알고리즘을 적용.',
    'IJK 주기성 등 생체신호의 수학적 모델링으로 도메인 피처를 구성.',
    '고급 노이즈 제거 기법을 적용해 전처리 파이프라인을 개선하고 신호 대 잡음비와 입력 특성의 견고성을 향상.',
    'AI 알고리즘 적용 전에는 강아지의 떨림이나 움직임으로 인해 심박 측정이 불안정했으나, 적용 후 정확도를 96%까지 향상.',
    '하드웨어 및 생산팀과 협업하여 데이터 수집 효율과 신호 품질을 최적화.',
    '수의 헬스 모니터링 웨어러블 디바이스 Sense1 Vet 개발에 기여.',
  ];

  const law_ENG = [
    "Developing a Legal AI Assistant that combines LLM (Llama-3-8B) with Retrieval-Augmented Generation (RAG) to specialize in legal queries.",
    "Implementing advanced prompt engineering techniques (zero-shot, few-shot, role-based, CoT) to improve response accuracy and context awareness in legal reasoning.",
    "Optimizing through high-quality preprocessing: cleaning, normalizing, and chunking legal texts to align the assistant with domain-specific terminology and reasoning.",
    "Designing a pipeline that integrates legal document chunking, vector embeddings (bge-m3), and FAISS-based semantic search, with Llama-3-8B as the core reasoning and generation engine. Extended this by building end-to-end implementation with 1024-dimensional embeddings, ChromaDB indexing, FastAPI serving, and AWS EC2/Docker deployment.",
    "Architecting the system with LangChain-based Agent orchestration, enabling modular coordination of retrieval, reasoning, document drafting, and strategy simulation.",
    "Applying Multi-Context Processing (MCP) to aggregate heterogeneous contexts (statutes, precedents, prior queries, user constraints) and enable integrated legal reasoning across sources.",
    "Tool routing with LangChain Agents: dynamic selection of retrievers, re-rankers, calculators, and citation formatters based on task intent and intermediate observations.",
    "Memory design for session-level personalization: caching retrieved authorities, maintaining working assumptions, and reusing verified citations across multi-turn interactions.",
    "Building a robust evaluation framework to measure factual consistency, legal validity, and user trust in AI-generated responses.",
    "Advanced prompting to upgrade intelligent legal research and strategy simulation: Chain-of-Thought for step-wise reasoning; role-based prompting (plaintiff, defendant, bench) for perspective shifting; ReAct (Reason + Act) to alternate retrieval and reasoning.",
    "Iterative RAG workflow: statutes/precedents retrieval → structured reasoning → follow-up retrieval (gap-filling) → conclusion with explicit citations and source attributions.",
    "Primary data provenance: full-text Korean statutes and precedents approved for use from the National Law Information System (Korea), extracted and normalized into a clean text corpus."
  ];

  const law_KOR = [
    "LLM(Llama-3-8B)과 Retrieval-Augmented Generation(RAG)을 결합해 법률 질의에 특화된 법률 AI 어시스턴트 개발.",
    "제로샷·퓨샷·역할 기반·CoT 등 고급 프롬프트 엔지니어링을 적용하여 법률 추론의 정확도와 맥락 인지를 향상.",
    "법령·판례 텍스트를 정제·정규화·청킹하여 도메인 특화 용어와 추론 방식에 맞춘 고품질 전처리로 성능 최적화.",
    "문서 청킹/임베딩(bge-m3)/FAISS 시맨틱 검색 파이프라인을 설계하고, 핵심 추론·생성 엔진으로 Llama-3-8B를 활용. 여기에 1024차원 임베딩 생성, ChromaDB 인덱싱, FastAPI 서빙, AWS EC2·Docker 배포까지 엔드투엔드 구현.",
    "LangChain 기반 에이전트 오케스트레이션으로 Retrieval·추론·문서 작성·전략 시뮬레이션 등 모듈을 유연하게 조율.",
    "Multi-Context Processing(MCP) 구조를 적용하여 법령·판례·질의 이력·사용자 제약 등 이질적 컨텍스트를 병렬로 수집·통합해 일관된 법리 추론을 수행.",
    "LangChain 에이전트의 툴 라우팅을 통해 태스크 의도와 중간 관찰값에 따라 리트리버·리랭커·계산기·인용 포맷터 등을 동적으로 선택.",
    "세션 메모리 설계로 다회차 상호작용에서 검증된 인용과 작업 가정을 재사용하고, 사용자 맞춤형 문서 흐름을 유지.",
    "사실 일치성·법적 타당성·사용자 신뢰도를 측정하는 평가 프레임워크를 구축하고, 결과를 기반으로 프롬프트·리트리버·리랭커를 지속 개선.",
    "추론 강화(CoT)·역할 기반 프롬프팅(원고·피고·재판부)·ReAct(Reason + Act)로 검색과 추론을 교대로 수행하여 리서치와 전략 시뮬레이션을 고도화.",
    "RAG 반복 흐름: 법령/판례 검색 → 구조화된 추론 → 추가 검색(정보 공백 보완) → 근거(출처) 명시 결론 도출.",
    "데이터 출처: 국가법령정보시스템의 승인된 본문 데이터를 활용해 정제·정규화된 한국어 법률 코퍼스 구축."
  ];

  const therapy_ENG = [
    "Developing a therapy-oriented AI assistant integrating Speech-to-Text (STT) and Text-to-Speech (TTS) pipelines to enable natural conversational interfaces.",
    "Built the front-end with React Native for cross-platform mobile deployment, focusing on real-time responsiveness and accessibility.",
    "Leveraged IBM Watsonx for model selection and orchestration, ensuring scalable integration of domain-specific LLMs.",
    "Implemented Retrieval-Augmented Generation (RAG) to ground therapeutic responses on validated resources and knowledge bases.",
    "Applied advanced prompt engineering and tuning strategies to adapt model outputs for counseling and therapy-like scenarios.",
    "Designed a robust evaluation pipeline measuring response empathy, factual consistency, and therapeutic appropriateness."
  ];
  const therapy_KOR = [
    "STT/TTS 파이프라인을 통합해 자연스러운 대화형 인터페이스를 제공하는 테라피 지향 AI 어시스턴트 개발.",
    "React Native 기반 크로스플랫폼 모바일 프론트엔드 구현(실시간 응답성/접근성 중점).",
    "IBM Watsonx로 모델 선정/오케스트레이션을 수행, 도메인 LLM의 확장 가능 통합 보장.",
    "검증된 자료/지식베이스에 기반한 RAG 구현으로 응답 신뢰도 확보.",
    "상담 시나리오 적합성을 높이기 위한 고급 프롬프트 튜닝 적용.",
    "공감·사실성·치료 적합성 지표로 평가 파이프라인 설계."
  ];

  // ===== Other Projects (이미지 포함) =====
  const eliza_media = (
    <div key="Eliza-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={elizaImage1} alt="Eliza Project 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={elizaImage2} alt="Eliza Project 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={elizaImage3} alt="Eliza Project 3" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const eliza_ENG = [
    'Developed an AI chatbot in Java using a scripting system with keywords, decomposition rules, and reassembly rules, simulating three personalities: a psychologist, a politician, and a five-year-old child. Implemented pre and post substitutions using regex for sentence transformation and synonym handling.',
    'Structured the chatbot engine into modular Java classes, including an Eliza Engine (managing input processing and response generation), a Decomposition Engine (applying regex-based pattern matching), and a Reassembly Engine (constructing responses with predefined grammatical structures).',
    'Implemented priority-based keyword matching, ensuring responses aligned with conversational context. Used regular expressions (regex) for pattern recognition, allowing dynamic sentence decomposition and reassembly for natural conversations.',
    'Collaborated using Mercurial for version control, managing project updates. Resolved merge conflicts with commands like hg resolve --all and hg merge, and manually edited clashing files for synchronization.',
    'Conducted iterative testing, refining keyword priorities to improve chatbot accuracy and ensuring smooth response flow. Identified challenges like post-substitution issues, where responses sometimes lacked precision, and planned improvements for more nuanced conversation handling.',
  ];
  const eliza_KOR = [
    'Java로 키워드·분해 규칙·재조립 규칙 기반 스크립팅 시스템을 구현, 심리학자/정치인/5세 어린이 3개 페르소나를 시뮬레이션. 정규식을 활용한 전/후 치환으로 문장 변환·동의어 처리.',
    'Eliza Engine(입력 처리/응답 생성), Decomposition Engine(정규식 패턴 매칭), Reassembly Engine(규칙 기반 응답 구성) 등 모듈형 아키텍처.',
    '우선순위 기반 키워드 매칭과 정규식 패턴 인식으로 문장 분해·재조립을 동적으로 수행.',
    'Mercurial 기반 협업/버전관리, 충돌 해결(hg resolve/merge) 및 수동 편집.',
    '반복 테스트로 키워드 우선순위를 다듬어 정확도 향상 및 응답 흐름 개선; 후치환 이슈 등 개선 과제 도출.',
  ];

  const royal_media = (
    <div key="RoyalUr-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={royalUrImage1} alt="RoyalUr Project 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={royalUrImage2} alt="RoyalUr Project 2" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const royal_ENG = [
    'Developed a digital version of the ancient board game "Royal Game of Ur" as part of a major university project.',
    'Implemented advanced game logic, AI opponents, and an interactive user interface to simulate strategic gameplay.',
    'Focused on enhancing user experience through a well-designed UI and optimized game mechanics.',
  ];
  const royal_KOR = [
    '고대 보드게임 “Royal Game of Ur”의 디지털 버전 개발(대학 메이저 프로젝트).',
    '고급 게임 로직/AI 상대/인터랙티브 UI를 구현해 전략적 플레이 시뮬레이션.',
    'UI/게임 메커닉스 최적화로 사용자 경험 강화.',
  ];

  const sudoku_media = (
    <div key="sudoku-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={sudokuImage1} alt="Sudoku Project 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={sudokuImage2} alt="Sudoku Project 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={sudokuImage3} alt="Sudoku Project 3" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={sudokuImage4} alt="Sudoku Project 4" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={sudokuImage5} alt="Sudoku Project 5" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const sudoku_ENG = [
    'Developed a collaborative Sudoku puzzle platform that allows users to create, share, and play puzzles.',
    'Designed and built the front-end with React.js, leveraging its flexibility, performance, and rich ecosystem. Implemented lifecycle methods to resolve rendering issues.',
    'Implemented a Node.js and Express.js backend, prioritizing speed, scalability, and security. Managed environment variables for secure authentication and database integration.',
    'Utilized MariaDB as the relational database, implementing primary and foreign keys for structured data relationships and efficient querying.',
    'Followed Agile development (Scrum methodology), utilizing sprints to ensure continuous progress and iterative development.',
    'Engineered advanced Sudoku generation and validation algorithms, supporting multiple difficulty levels for an engaging user experience.',
    'Designed and implemented the front-end using React.JS, chosen for its flexibility, performance, and extensive ecosystem. Addressed rendering issues by utilizing lifecycle methods to correctly update puzzle states.',
  ];
  const sudoku_KOR = [
    '사용자들이 스도쿠 퍼즐을 제작/공유/플레이할 수 있는 협업 플랫폼 개발.',
    'React.js 프론트엔드 설계·구현(성능/생태계 활용), 라이프사이클로 렌더링 이슈 해결.',
    'Node/Express 백엔드로 속도·확장성·보안 확보, 환경변수로 인증/DB 연동 관리.',
    'MariaDB(관계형)로 PK/FK 모델링·효율적 질의 설계.',
    '애자일(Scrum) 기반 스프린트로 반복적 개발/개선.',
    '난이도 조절 가능한 생성/검증 알고리즘으로 UX 강화.',
    '렌더링 상태 동기화 개선으로 프론트 안정화.',
  ];

  const aura_media = (
    <div key="auraid-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={auraIdIamge1} alt="AuraId Project 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={auraIdIamge7} alt="AuraId Project 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={auraIdIamge2} alt="AuraId Project 3" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={auraIdIamge3} alt="AuraId Project 4" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={auraIdIamge4} alt="AuraId Project 5" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={auraIdIamge5} alt="AuraId Project 6" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={auraIdIamge6} alt="AuraId Project 7" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const aura_ENG = [
    'Developed a web-based dog recognition platform using TypeScript with React, implementing an advanced backend algorithm developed by Jeju Nationaly University for accurate dog identification based on image recognition technology.',
    'Designed and implemented a veterinary hospital management system, enabling efficient patient tracking and cage record management for veterinarians.',
    'Integrated AWS RDS (Relational Database Service) for secure, scalable data management, ensuring seamless data retrieval and storage for both the dog recognition platform and the hospital management system.',
  ];
  const aura_KOR = [
    'TypeScript/React 기반 반려견 인식 웹 플랫폼 개발(제주대 알고리즘 연동으로 정확도 강화).',
    '수의사 대상 병원 관리 시스템 설계/구현(환자 추적, 케이지 기록 관리).',
    'AWS RDS로 보안/확장성 보장, 플랫폼·병원 시스템 공용 데이터 파이프라인 구축.',
  ];

  // ===== Achievements =====
  const dacon = (
    <div key="dacon-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={daconImage1} alt="Dacon Competition 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={daconImage2} alt="Dacon Competition 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={daconImage3} alt="Dacon Competition 3" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={daconImage4} alt="Dacon Competition 4" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={daconImage5} alt="Dacon Competition 5" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const ach_dacon_ENG = [
    "Actively participated in multiple Dacon competitions covering both structured and unstructured datasets.",
    "Gained hands-on experience with diverse machine learning models including DNN, CNN, and RNN across different problem domains.",
    "Explored LLM applications by joining prompt engineering–focused competitions."
  ];

  const ach_dacon_KOR = [
    "정형·비정형 데이터를 아우르는 다수의 Dacon 대회에 적극 참여.",
    "DNN, CNN, RNN 등 다양한 머신러닝 모델을 활용하며 여러 문제 영역을 경험.",
    "LLM 프롬프트 엔지니어링 대회에도 참가하여 활용 가능성을 탐구."
  ];

  const quantum_media = (
    <div key="quantum-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
      <img src={quantumImage4} alt="Quantum AI Hackathon 4" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={quantumImage1} alt="Quantum AI Hackathon 1" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={quantumImage2} alt="Quantum AI Hackathon 2" style={{ height: '400px', borderRadius: '8px' }} />
      <img src={quantumImage3} alt="Quantum AI Hackathon 3" style={{ height: '400px', borderRadius: '8px' }} />
    </div>
  );
  const quantum_ENG = [
    "Qualified for the finals by ranking 1st place in the AI Factory preliminary competition, solving a Fashion-MNIST quantum computing challenge through coding.",
    "Participated in a 1-night, 2-day hackathon focused on Quantum Computing and Artificial Intelligence.",
    "Competed in advanced problem-solving sessions combining quantum algorithms with AI-driven approaches.",
    "Awarded the Excellence Prize (우수상) for innovative application of quantum AI methods.",
    "Collaborated with peers to explore practical use cases of quantum machine learning and optimization.",
  ];
  const quantum_KOR = [
    "AI Factory 예선(패션-MNIST 양자 과제) 1위로 본선 진출.",
    "양자컴퓨팅·AI 주제의 1박 2일 해커톤 참가.",
    "양자 알고리즘과 AI 접근을 결합한 고난도 문제 해결 세션 수행.",
    "양자 AI 응용의 혁신성으로 우수상 수상.",
    "동료들과 양자 ML/최적화의 실사용 사례를 탐구.",
  ];

  const ach_quantum_ENG = [
    'Ranked 1st in the qualifying round with a coding-based Fashion-MNIST quantum computing challenge.',
    'Advanced to the finals; awarded the Excellence Prize for innovative application of quantum AI methods.',
  ];
  const ach_quantum_KOR = [
    '패션-MNIST 양자 과제로 예선 1위, 본선 진출.',
    '양자 AI 응용 혁신성으로 우수상 수상.',
  ];

  const ach_kaggle_ENG = [
    'Achieved Top 3% using an EDA → feature engineering → ensemble pipeline (GBDT + stacking).',
    'Ensured reproducibility and leaderboard stability with robust seeding and well-designed K-Fold validation.',
  ];
  const ach_kaggle_KOR = [
    'EDA → 피처 엔지니어링 → 앙상블(GBDT+스태킹) 파이프라인으로 상위 3% 달성.',
    '시드 고정/K-Fold 설계로 재현성·리더보드 안정성 확보.',
  ];

  
  const ach_ces_ENG = [
    'Led the wearable animal health monitoring project for live demos and partner engagements.',
    'Crafted technical/product storytelling, demo flow, and coordinated global partner meetings.',
  ];
  const ach_ces_KOR = [
    '웨어러블 동물 헬스 모니터링 프로젝트 리드(라이브 데모/파트너 밋업).',
    '기술/제품 스토리텔링과 데모 동선 설계, 글로벌 파트너 미팅 주도.',
  ];

  // ===== Skills 컴포넌트 & 데이터 =====
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
  const skillsData = {
    ENG: [
      { title: "AI & Machine Learning", items: [
        { Icon: SiPytorch, label: "PyTorch" },
        { Icon: SiTensorflow, label: "TensorFlow" },
        { Icon: SiKeras, label: "Keras" },
        { Icon: SiNumpy, label: "NumPy" },
        { Icon: SiPandas, label: "Pandas" },
        { Icon: SiOpenai, label: "Large Language Models (LLM)" },
      ]},
      { title: "Programming Language", items: [
        { Icon: SiPython, label: "Python" },
        { Icon: FaJava, label: "Java" },
        { Icon: SiJavascript, label: "JavaScript" },
        { Icon: SiTypescript, label: "TypeScript" },
        { Icon: SiKotlin, label: "Kotlin" },
        { Icon: SiDart, label: "Dart" },
      ]},
      { title: "App / Web Framework", items: [
        { Icon: SiReact, label: "React" },
        { Icon: SiFlutter, label: "Flutter" },
      ]},
      { title: "Database", items: [
        { Icon: SiMysql, label: "MySQL" },
        { Icon: SiMongodb, label: "MongoDB" },
        { Icon: SiPostgresql, label: "PostgreSQL" },
      ]},
      { title: "Workflow & Tools", items: [
        { Icon: SiGit, label: "Git" },
        { Icon: SiJira, label: "Jira" },
        { Icon: SiSlack, label: "Slack" },
        { Icon: SiFigma, label: "Figma" },
        { Icon: SiDocker, label: "Docker" } 
      ]},
      { title: "Languages", items: [
        { Icon: SiJavascript, label: "English (Native)" },
        { Icon: SiReact, label: "Korean (Native)" },
      ]},
    ],
    KOR: [
      { title: "AI & 머신러닝", items: [
        { Icon: SiPytorch, label: "PyTorch" },
        { Icon: SiTensorflow, label: "TensorFlow" },
        { Icon: SiKeras, label: "Keras" },
        { Icon: SiNumpy, label: "NumPy" },
        { Icon: SiPandas, label: "Pandas" },
        { Icon: SiOpenai, label: "대형 언어모델 (LLM)" },
      ]},
      { title: "프로그래밍 언어", items: [
        { Icon: SiPython, label: "Python" },
        { Icon: FaJava, label: "Java" },
        { Icon: SiJavascript, label: "JavaScript" },
        { Icon: SiTypescript, label: "TypeScript" },
        { Icon: SiKotlin, label: "Kotlin" },
        { Icon: SiDart, label: "Dart" },
      ]},
      { title: "앱 / 웹 프레임워크", items: [
        { Icon: SiReact, label: "React" },
        { Icon: SiFlutter, label: "Flutter" },
      ]},
      { title: "데이터베이스", items: [
        { Icon: SiMysql, label: "MySQL" },
        { Icon: SiMongodb, label: "MongoDB" },
        { Icon: SiPostgresql, label: "PostgreSQL" },
      ]},
      { title: "워크플로 & 도구", items: [
        { Icon: SiGit, label: "Git" },
        { Icon: SiJira, label: "Jira" },
        { Icon: SiSlack, label: "Slack" },
        { Icon: SiFigma, label: "Figma" },
        { Icon: SiDocker, label: "Docker" }
      ]},
      { title: "언어", items: [
        { Icon: SiJavascript, label: "영어 (원어민)" },
        { Icon: SiReact, label: "한국어 (원어민)" },
      ]},
    ],
  };

  // ===== UI =====
  return (
    <div className="App">
      <header className="App-header">
        <h1>{t[lang].headerTitle}</h1>

        {/* Language Toggle */}
        <div className="lang-toggle" aria-label="Language toggle" style={{ margin:'6px 0 10px' }}>
          <div
            className="lang-indicator"
            style={{ transform: `translateX(${lang === 'ENG' ? '0' : '100%'})` }}
          />
          <button
            className={`lang-btn ${lang === 'ENG' ? 'active' : ''}`}
            onClick={() => setLang('ENG')}
          >
            ENG
          </button>
          <button
            className={`lang-btn ${lang === 'KOR' ? 'active' : ''}`}
            onClick={() => setLang('KOR')}
          >
            KOR
          </button>
        </div>

        <div className="contact-icons">
          <a href="mailto:peter.jaewoochang@gmail.com" aria-label="Email">
            <FaEnvelope size={30} style={{ margin: '0 15px', color: '#000' }} />
          </a>
          <a href="tel:+821074465388" aria-label="Phone">
            <FaPhone size={30} style={{ margin: '0 15px', color: '#000' }} />
          </a>
          <a href="https://github.com/jwc5388" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
            <FaGithub size={30} style={{ margin: '0 15px', color: '#000' }} />
          </a>
          <a href="https://www.linkedin.com/in/jwcbillion33" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <FaLinkedin size={30} style={{ margin: '0 15px', color: '#000' }} />
          </a>
        </div>
      </header>


      {/* ===== Education ===== */}
      <section className="Education-section">
        <h2 onClick={() => toggleSection('education')}>{t[lang].education}</h2>
        {expandedSections.education.expanded && (
          <div className="section-content">
            <Entry
              title={lang==='ENG' ? "University of St Andrews, St Andrews, Scotland" : "세인트앤드루스 대학교, 스코틀랜드"}
              location={lang==='ENG' ? "Bachelor of Science in Mathematics and Computer Science" : "수학·컴퓨터과학 학사"}
              dates={lang==='ENG' ? "September 2019 - June 2024" : "2019년 9월 - 2024년 6월"}
              details={[
                <div key="dissertation1" className="download-link">
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); window.open(dissertation1, '_blank', 'noopener'); }}
                    style={{ background:'transparent', border:0, padding:0, cursor:'pointer' }}
                  >
                    <img src={dissImage} alt="Open Dissertation 1" className="download-icon" />
                  </button>
                  <span>{lang==='ENG' ? "Computer Science Dissertation" : "컴퓨터과학 학위논문"}</span>
                </div>,
                <div key="dissertation2" className="download-link">
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); window.open(dissertation2, '_blank', 'noopener'); }}
                    style={{ background:'transparent', border:0, padding:0, cursor:'pointer' }}
                  >
                    <img src={dissImage} alt="Open Dissertation 2" className="download-icon" />
                  </button>
                  <span>{lang==='ENG' ? "Mathematics Dissertation" : "수학 학위논문"}</span>
                </div>,
                <div key="graduation-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
                  <img src={dissertationImage1} alt="dissertation1" style={{ height: '400px', borderRadius: '8px' }} />
                  <img src={dissertationImage2} alt="dissertation2" style={{ height: '400px', borderRadius: '8px' }} />
                  <img src={degreeImage} alt="Graduation" style={{ height: '400px', borderRadius: '8px' }} />
                </div>
              ]}
              isExpanded={expandedSections.education.entries.degree}
              onClick={() => toggleEntry('education', 'degree')}
            />

            <Entry
              title="[IBM x RedHat] AI Transformation - AX Academy"
              location="IBM x RedHat"
              dates={lang==='ENG' ? "April 2025 ~ Present" : "2025.04 ~ 진행중"}
              details={[
                ...(lang==='ENG'
                  ? [
                      "Participated in the AI Transformation program hosted by IBM and RedHat.",
                      "Hands-on learning with TensorFlow, Keras, and PyTorch; built and experimented with DNN, CNN, RNN, and NLP models.",
                      "Studied and applied insights from AI dissertations, including Attention Is All You Need, GPT 1,2,3 and BERT.",
                      "Learned advanced LLM applications directly from IBM developers, focusing on RAG and Prompt Engineering.",
                      "Actively participated in multiple AI-related competitions: Dacon challenges, hackathons, and collaborative projects.",
                      "Currently leading the final IBM presentation project: developing a Legal AI Assistant powered by LLM."
                    ]
                  : [
                      "IBM/RedHat 주관 AI Transformation 프로그램 참여.",
                      "TensorFlow, Keras, PyTorch를 활용해 DNN, CNN, RNN, NLP 모델 학습 및 실습.",
                      "Attention Is All You Need, Semantic Structure in Large Language Model Embeddings, YOLO, BERT 등 주요 논문을 학습하고 적용.",
                      "현직 IBM 개발자에게 LLM(RAG, Prompt Engineering) 심화 강의 수강.",
                      "Dacon 대회, 해커톤 등 다수의 AI 관련 대회에 적극적으로 참가.",
                      "과정 최종 단계로 IBM 발표용 팀 프로젝트 진행 중: 법률 AI Assistant LLM 개발."
                    ]),
                // 이미지 블록
                <div key="ibm-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
                  <img src={ibmImage1} alt="IBM x RedHat 1" style={{ height: '400px', borderRadius: '8px' }} />
                  {/* <img src={ibmImage2} alt="IBM x RedHat 2" style={{ height: '400px', borderRadius: '8px' }} /> */}
                </div>
              ]}
              isExpanded={expandedSections.education.entries.ibmAxAcademy}
              onClick={() => toggleEntry('education', 'ibmAxAcademy')}
            />
            <Entry
              title={lang==='ENG' ? "St Andrews Judo Club / Registered as member of Judo Scotland" : "세인트앤드루스 유도부 / Judo Scotland 등록 회원"}
              location=""
              dates=""
              details={[
                <div key="judo-images" style={{ display:'flex', overflowX:'auto', whiteSpace:'nowrap', gap:'10px', padding:'10px 0' }}>
                  <img src={judoImage1} alt="Judo Image 1" style={{ height: '400px', borderRadius: '8px' }} />
                  <img src={judoImage2} alt="Judo Image 2" style={{ height: '400px', borderRadius: '8px' }} />
                  <img src={judoImage3} alt="Judo Image 3" style={{ height: '400px', borderRadius: '8px' }} />
                </div>
              ]}
              isExpanded={expandedSections.education.entries.judo}
              onClick={() => toggleEntry('education', 'judo')}
            />
            <Entry
              title={lang==='ENG' ? "Committee member of St Andrews Korean Society" : "세인트앤드루스 한인회 운영진"}
              location={lang==='ENG' ? "Treasurer for St Andrews Korean Society" : "한인회 회계 담당"}
              details={[]}
              isExpanded={expandedSections.education.entries.society}
              onClick={() => toggleEntry('education', 'society')}
            />
          </div>
        )}
      </section>

      {/* ===== Work Experience ===== */}
      <section className="Experience-section">
        <h2 onClick={() => toggleSection('experience')}>{t[lang].work}</h2>
        {expandedSections.experience.expanded && (
          <div className="section-content">
            <Entry
              title={work_ai_title}
              location={lang==='ENG' ? "Seoul, South Korea" : "대한민국 서울"}
              dates="September 2024 - Present"
              details={lang==='ENG' ? work_ai_details_ENG : work_ai_details_KOR}
              isExpanded={expandedSections.experience.entries.aiAlgorithm}
              onClick={() => toggleEntry('experience', 'aiAlgorithm')}
            />
            {/* <Entry
              title={work_web_title}
              location={lang==='ENG' ? "Seoul, South Korea" : "대한민국 서울"}
              dates="February 2024 - Present"
              details={lang==='ENG' ? work_web_details_ENG : work_web_details_KOR}
              isExpanded={expandedSections.experience.entries.webDeveloper}
              onClick={() => toggleEntry('experience', 'webDeveloper')}
            /> */}
            <Entry
              title={work_app_title}
              location={lang==='ENG' ? "Jeju Island, South Korea" : "대한민국 제주"}
              dates="June 2023 - August 2023"
              details={lang==='ENG' ? work_app_details_ENG : work_app_details_KOR}
              isExpanded={expandedSections.experience.entries.appdeveloper}
              onClick={() => toggleEntry('experience', 'appdeveloper')}
            />
            <Entry
              title={work_math_title}
              location={lang==='ENG' ? "Jeju Island, South Korea" : "대한민국 제주"}
              dates="May 2022 - August 2022"
              details={lang==='ENG' ? work_math_details_ENG : work_math_details_KOR}
              isExpanded={expandedSections.experience.entries.mathematician}
              onClick={() => toggleEntry('experience', 'mathematician')}
            />

            {/* Company about */}
            <Entry
              title={t[lang].companyAbout}
              location={lang==='ENG' ? "Jeju Island, South Korea" : "대한민국 제주"}
              dates={t[lang].futureOfVet}
              details={[
                {
                  title: lang==='ENG' ? 'AI collar for future veterinary care' : '미래 수의학을 위한 AI 목걸이',
                  content: (
                    <div style={{ paddingBottom: '20px' }}>
                      <p>
                        {lang==='ENG'
                          ? "The AI collar developed by CareSix revolutionizes veterinary care by monitoring pets' health in real-time."
                          : "CareSix의 AI 목걸이는 반려동물의 건강을 실시간 모니터링하여 수의 진료를 혁신합니다."}
                      </p>
                      <img src={cotonsImage1} alt="CareSix AI Collar" style={{ height: '400px', borderRadius: '8px' }} />
                    </div>
                  ),
                },
                {
                  title: lang==='ENG' ? 'Awards' : '수상',
                  content: (
                    <div>
                      {company_awards_media}
                      <ul>
                        {(lang==='ENG' ? company_awards_list_ENG : company_awards_list_KOR)
                          .map((x, i)=><li key={i}>{x}</li>)}
                      </ul>
                    </div>
                  ),
                },
                {
                  title: t[lang].companyMore,
                  content: (
                    <div>
                      <p>
                        {lang==='ENG'
                          ? "CareSix is at the forefront of pet healthcare technology. Learn more on their "
                          : "CareSix는 반려동물 헬스케어 테크를 선도합니다. 더 보려면 "}
                        <a href="https://cotons.ai" target="_blank" rel="noopener noreferrer">
                          {t[lang].officialSite}
                        </a>.
                      </p>
                    </div>
                  ),
                },
              ]}
              isExpanded={expandedSections.experience.entries.caresix}
              onClick={() => toggleEntry('experience', 'caresix')}
            />
          </div>
        )}
      </section>

      {/* ===== Projects ===== */}
      <section className="Project-section">
        <h2 onClick={() => toggleSection('projects')}>{t[lang].projects}</h2>
        {expandedSections.projects.expanded && (
          <div className="section-content">

            {/* Main Projects – 항상 표시 */}
            <h3 style={{ marginTop: 0 }}>{t[lang].mainProjects}</h3>

            <Entry
              title={lang==='ENG' ? "Sense1 Vet AI Algorithm" : "Sense1 Vet AI 알고리즘"}
              location={lang==='ENG' ? "CareSix Co., LTD" : "케어식스"}
              dates={lang==='ENG' ? "September 2024 ~ February 2025" : "2024.09 ~ 2025.02"}
              details={getDetails(pj_sense1_ENG, pj_sense1_KOR, sense1_media)}
              isExpanded={expandedSections.projects.entries.sense1Vet}
              onClick={() => toggleEntry('projects', 'sense1Vet')}
            />

            <Entry
              title="[IBM x RedHat] Law-AI"
              location={lang==='ENG' ? "IBM Final Group Project" : "IBM 파이널 그룹 프로젝트"}
              dates={lang==='ENG' ? "2025 ~ Present" : "2025 ~ 진행중"}
              details={lang==='ENG' ? law_ENG : law_KOR}
              isExpanded={expandedSections.projects.entries.lawIntelligence}
              onClick={() => toggleEntry('projects', 'lawIntelligence')}
            />

            {/* <Entry
              title="[IBM x RedHat] Therapy-Intelligence"
              location={lang==='ENG' ? "IBM x RedHat Innovation Project" : "IBM x RedHat 이노베이션 프로젝트"}
              dates={lang==='ENG' ? "2025 ~ Present" : "2025 ~ 진행중"}
              details={lang==='ENG' ? therapy_ENG : therapy_KOR}
              isExpanded={expandedSections.projects.entries.therapyIntelligence}
              onClick={() => toggleEntry('projects', 'therapyIntelligence')}
            /> */}

            {/* Other Projects – 클릭으로 펼침 */}
            <h3
              style={{ marginTop: 24, cursor:'pointer', userSelect:'none', display:'flex', alignItems:'center', justifyContent:'space-between' }}
              onClick={() => toggleEntry('projects', 'otherProjects')}
            >
              {t[lang].otherProjects}
              <span style={{ fontSize: 18 }}>
                {expandedSections.projects.entries.otherProjects ? t[lang].collapseUp : t[lang].collapseDown}
              </span>
            </h3>

            {expandedSections.projects.entries.otherProjects && (
              <div>
                <Entry
                  title="Eliza AI Basic Project"
                  location={lang==='ENG' ? "University Project" : "대학 프로젝트"}
                  dates={lang==='ENG' ? "September 2020 ~ December 2020" : "2020.09 ~ 2020.12"}
                  details={getDetails(eliza_ENG, eliza_KOR, eliza_media)}
                  isExpanded={expandedSections.projects.entries.eliza}
                  onClick={() => toggleEntry('projects', 'eliza')}
                />

                <Entry
                  title="Royal Game of Ur"
                  location={lang==='ENG' ? "University Project" : "대학 프로젝트"}
                  dates={lang==='ENG' ? "January 2021 ~ March 2021" : "2021.01 ~ 2021.03"}
                  details={getDetails(royal_ENG, royal_KOR, royal_media)}
                  isExpanded={expandedSections.projects.entries.royalGame}
                  onClick={() => toggleEntry('projects', 'royalGame')}
                />

                <Entry
                  title="Sudoku Game"
                  location={lang==='ENG' ? "University of St Andrews Computer Science Junior Honours Project" : "세인트앤드루스대 컴퓨터과학 3학년 프로젝트"}
                  dates={lang==='ENG' ? "September 2022 ~ March 2023" : "2022.09 ~ 2023.03"}
                  details={getDetails(sudoku_ENG, sudoku_KOR, sudoku_media)}
                  isExpanded={expandedSections.projects.entries.sudokuGame}
                  onClick={() => toggleEntry('projects', 'sudokuGame')}
                />

                <Entry
                  title="AURA ID Website"
                  location={lang==='ENG' ? "CareSix Co., LTD" : "케어식스"}
                  dates={lang==='ENG' ? "February 2025 ~ Present" : "2025.02 ~ 진행중"}
                  details={getDetails(aura_ENG, aura_KOR, aura_media)}
                  isExpanded={expandedSections.projects.entries.auraid}
                  onClick={() => toggleEntry('projects', 'auraid')}
                />
              </div>
            )}
          </div>
        )}
      </section>

      {/* ===== Engagements ===== */}
      <section className="Engagement-section">
        <h2 onClick={() => toggleSection('engagements')}>{t[lang].engagements}</h2>
        {expandedSections.engagements.expanded && (
          <div className="section-content">
            <Entry
              title="J-AGRI Exhibition, Tokyo"
              location={lang==='ENG' ? "Tokyo, Japan" : "일본 도쿄"}
              dates="October 9-11, 2024"
              details={getDetails(jAgri_ENG, jAgri_KOR, jAgri_media)}
              isExpanded={expandedSections.engagements.entries.jAgri}
              onClick={() => toggleEntry('engagements', 'jAgri')}
            />
            <Entry
              title="FAVA 2024 - 23rd Federation of Asian Veterinary Associations Congress"
              location={lang==='ENG' ? "Daejeon, South Korea" : "대한민국 대전"}
              dates="October 25-27, 2024"
              details={getDetails(fava_ENG, fava_KOR, fava_media)}
              isExpanded={expandedSections.engagements.entries.fava2024}
              onClick={() => toggleEntry('engagements', 'fava2024')}
            />
            <Entry
              title="CES 2025 Exhibition"
              location={lang==='ENG' ? "Las Vegas, USA" : "미국 라스베이거스"}
              dates="January 2025"
              details={getDetails(ces_ENG, ces_KOR, ces_media)}
              isExpanded={expandedSections.engagements.entries.ces2025}
              onClick={() => toggleEntry('engagements', 'ces2025')}
            />
            {/* <Entry
              title={lang==='ENG' ? "2025 Quantum AI Hackathon" : "2025 퀀텀 AI 해커톤"}
              location={lang==='ENG' ? "Jeonju University, South Korea" : "대한민국 전주대"}
              dates="August 18-19, 2025"
              details={getDetails(quantum_ENG, quantum_KOR, quantum_media)}
              isExpanded={expandedSections.engagements.entries.quantumAIHackathon}
              onClick={() => toggleEntry('engagements', 'quantumAIHackathon')}
            /> */}
          </div>
        )}
      </section>


      {/* ===== Achievements ===== */}
      <section className="Achievements-section">
        <h2 onClick={() => toggleSection('achievements')}>{t[lang].achievements}</h2>
        {expandedSections.achievements.expanded && (
          <div className="section-content">

            <Entry
              title={lang==='ENG' ? "2025 Quantum AI Hackathon" : "2025 퀀텀 AI 해커톤"}
              location={lang==='ENG' ? "Jeonju University, South Korea" : "대한민국 전주대"}
              dates="August 18-19, 2025"
              details={getDetails(quantum_ENG, quantum_KOR, quantum_media)}
              isExpanded={expandedSections.engagements.entries.quantumAIHackathon}
              onClick={() => toggleEntry('engagements', 'quantumAIHackathon')}
            />


            <Entry
              title={lang==='ENG' ? "2025 K-Digital Training AI Hackathon" : "2025 K-디지털 트레이닝 AI 해커톤"}
              location={lang==='ENG' ? "South Korea" : "대한민국"}
              dates="August 2025"
              details={getDetails(hackathon_ENG, hackathon_KOR, hackathon_media)}
              isExpanded={expandedSections.engagements.entries.kdigitalHackathon}
              onClick={() => toggleEntry('engagements', 'kdigitalHackathon')}
            />

            {/* <Entry
              title={lang==='ENG' ? "Kaggle Competition – Top 3%" : "Kaggle Competition – 상위 3%"}
              location="Global (Online)"
              dates="2024"
              details={lang==='ENG' ? ach_kaggle_ENG : ach_kaggle_KOR}
              isExpanded={expandedSections.achievements.entries.kaggleTop3}
              onClick={() => toggleEntry('achievements', 'kaggleTop3')}
            /> */}

            <Entry
              title={lang==='ENG' ? "Dacon AI Competitions" : "Dacon AI 대회"}
              location={lang==='ENG' ? "Korea (Online)" : "대한민국 (온라인)"}
              dates="May 2025-Present"
              details={getDetails(ach_dacon_ENG, ach_dacon_KOR, dacon)}
              isExpanded={expandedSections.engagements.entries.daconCompetitions}
              onClick={() => toggleEntry('engagements', 'daconCompetitions')}
            />

            {/* <Entry
              title={lang==='ENG' ? "CES Innovation Awards – Project Lead Participation" : "CES Innovation Awards – 프로젝트 리드 참여"}
              location={lang==='ENG' ? "Las Vegas, USA" : "미국 라스베이거스"}
              dates="2025"
              details={lang==='ENG' ? ach_ces_ENG : ach_ces_KOR}
              isExpanded={expandedSections.achievements.entries.cesInnovation}
              onClick={() => toggleEntry('achievements', 'cesInnovation')}
            /> */}
          </div>
        )}
      </section>


      {/* ===== Skills (아이콘 카드) ===== */}
      <section className="Skills-section">
        <h2 onClick={() => toggleSection('skills')}>{t[lang].skills}</h2>
        {expandedSections.skills.expanded && (
          <div className="section-content">
            <div className="skills-grid">
              {skillsData[lang].map((g, i) => (
                <SkillGroup key={i} title={g.title} items={g.items} />
              ))}
            </div>
          </div>
        )}
      </section>



      

      {/* Volunteer 섹션은 주석 상태 */}
    </div>
  );
}

export default App;