export const portfolioData = {
  ko: {
    locale: "ko",
    hero: {
      name: "장우진",
      title: "AI 엔지니어 · 풀스택 빌더",
      tagline: "TensorFlow·PyTorch 모델링과 LLM·RAG 제품화를 잇는 실전형 AI 개발자",
      summary:
        "TensorFlow·PyTorch 기반 모델 실험과 LangChain·FastAPI·AWS로 이어지는 LLM·RAG 서비스를 구축합니다. IBM x Red Hat AI Transformation 과정 우수훈련생으로 선발되어 법률 도메인 RAG, 멀티 에이전트, Docker 배포까지 6개월 풀타임으로 완주했으며, Toss NEXT ML Challenge 20위(2,591팀), 퀀텀 AI 경진대회 우수상 등으로 실전 성과를 입증했습니다.",
      highlights: [
        "Transformer / LLM · RAG",
        "Prompt Engineering",
        "MLOps (AWS·Docker·PostgreSQL)",
        "TensorFlow · PyTorch",
      ],
      stats: [
        { label: "수상", value: "퀀텀 AI 경진대회 우수상" },
        { label: "대회 성과", value: "Toss NEXT ML 20위 / 2,591팀" },
        { label: "교육", value: "IBM x Red Hat AI Transformation 우수훈련생" },
      ],
      quickFacts: [
        { label: "Email", value: "wjj9319@gmail.com", href: "mailto:wjj9319@gmail.com" },
        { label: "GitHub", value: "github.com/wing0907", href: "https://github.com/wing0907" },
        { label: "LinkedIn", value: "linkedin.com/in/wjinj", href: "https://www.linkedin.com/in/wjinj" },
        { label: "주소", value: "(04996) 서울 광진구 군자로" },
        { label: "출생", value: "1993년 · 남" },
        { label: "언어", value: "한국어, 영어(필리핀·캐나다 장기 체류)" },
      ],
    },
    sections: [
      {
        id: "strengths",
        title: "핵심 역량",
        layout: "bullets",
        items: [
          "법령·산업 데이터 기반 LLM·RAG, LangChain/LangGraph 에이전트 설계와 근거 대시보드 구현",
          "TensorFlow·PyTorch, Optuna, W&B, K-Fold/OOF, Platt/Isotonic으로 재현 가능한 모델 실험 설계",
          "FastAPI·Docker·AWS(EC2/S3)·Nginx 기반 추론 파이프라인 구축과 지연·원가 최적화",
          "데이터 전처리 스냅샷, 자동 리포트, 실험 템플릿으로 MLOps 표준화 및 협업 생산성 향상",
          "필리핀·캐나다 장기 유학으로 영어 커뮤니케이션·문서화·현지 협업 역량 보유",
        ],
      },
      {
        id: "skills",
        title: "기술 스택",
        layout: "columns",
        columns: [
          {
            title: "데이터 & 스토리지",
            items: ["PostgreSQL", "ChromaDB / FAISS", "PyArrow / Parquet", "Pandas"],
          },
          {
            title: "서빙 & 백엔드",
            items: ["FastAPI", "Node.js / Express", "Nginx", "Streamlit"],
          },
          {
            title: "인프라 & Ops",
            items: ["Docker", "AWS EC2 / S3", "CUDA", "Linux / Ubuntu"],
          },
          {
            title: "모델링 & 실험",
            items: ["Optuna", "Weights & Biases", "K-Fold / OOF", "Platt / Isotonic Calibration"],
          },
          {
            title: "비전 & 검출",
            items: ["YOLO 계열", "ViT / Swin v2", "SAM2", "OpenCV"],
          },
          {
            title: "협업 & 도구",
            items: ["LangChain / LangGraph", "GitHub", "Slack", "Figma", "VSCode"],
          },
        ],
      },
      {
        id: "experience",
        title: "경험 · 교육",
        layout: "stack",
        items: [
          {
            title: "[IBM x Red Hat] AI Transformation",
            subtitle: "우수훈련생 · 장려상 (6개월 풀타임)",
            period: "2025.05 – 2025.11",
            location: "대한민국 (온·오프라인)",
            bullets: [
              "TensorFlow·PyTorch 기반 DNN/CNN/RNN 실전 과제와 LLM·RAG 에이전트 오케스트레이션 심화",
              "FastAPI·Docker·AWS 배포 파이프라인, HTML/JavaScript, LangChain·LangGraph 실습",
              "AutoEncoder, YOLO, ViT, SAM2, Swin Transformer 등 논문 구현과 프롬프트 엔지니어링 고도화",
            ],
          },
          {
            title: "Seneca College, Flight Services – Cabin Operations & Management",
            subtitle: "2·3년제 대학 · GPA 4.0/4.0 · 졸업",
            period: "2019.05 – 2020.10",
            location: "토론토, 캐나다",
            bullets: [
              "Amadeus 수업 조교 및 동료 튜터링으로 리더십·커뮤니케이션 역량 강화",
              "영어 기반 서비스 운영·위기 대응 커리큘럼으로 매뉴얼 제작 및 문서화 역량 확보",
            ],
          },
          {
            title: "글로벌 현지 경험",
            subtitle: "필리핀·캐나다 장기 유학 · 통역 · 현지 근무",
            period: "2003.01 – 2024.10",
            location: "필리핀 · 캐나다",
            bullets: [
              "KOTRA 행사 통역, 현지 기업 커뮤니케이션 및 협업 경험",
              "요식·환경·건설 분야 근무로 다문화 조직 내 실무 경험 축적",
              "영어·따갈로그 사용으로 기술 문서와 논문 커뮤니케이션 즉시 수행",
            ],
          },
        ],
      },
      {
        id: "projects",
        title: "대표 프로젝트",
        layout: "stack",
        items: [
          {
            title: "팀 레모네이드 LAWAI",
            subtitle: "법률 도메인 LLM 비서 · 5명 팀",
            period: "2025.09.08 – 11.07",
            location: "React · FastAPI · AWS · Docker",
            bullets: [
              "Llama-3-8B + bge-m3 임베딩, Chroma·FAISS·BM25 하이브리드로 판례·법령 RAG 설계",
              "LangChain 에이전트(검색·작성·검토)와 세션 메모리, 증거 카드·재랭킹·대시보드 구현",
              "FastAPI·Docker·AWS EC2 배포, React UI와 근거 기반 대화 UX 설계",
            ],
            tags: ["LLM", "RAG", "LangChain", "FastAPI", "Docker", "AWS", "React"],
            links: [
              { label: "Architecture & Gallery", href: "/assets/lawai/gallery.html" },
              { label: "GitHub", href: "https://github.com/wing0907" },
            ],
          },
          {
            title: "GitHub 개인 연구 저장소",
            subtitle: "Transformer · Diffusion · Vision 실험",
            period: "2025.10.01 – 10.20",
            location: "Solo",
            bullets: [
              "LLM 프롬프트 실험과 LangGraph 기반 멀티 에이전트 시나리오 구현",
              "Transformer, ViT, YOLO 계열 논문 재현 코드와 실험 로그 정리",
              "데이터 전처리 파이프라인과 자동화 스크립트 공유로 팀 온보딩 가속",
            ],
            tags: ["LLM", "Transformer", "Computer Vision", "LangGraph"],
            links: [{ label: "GitHub Profile", href: "https://github.com/wing0907" }],
          },
        ],
      },
      {
        id: "research",
        title: "논문 구현 시리즈",
        layout: "cards",
        items: [
          {
            title: "Transformer 논문 구현",
            period: "2025.09.08 – 09.12 · 5명",
            bullets: [
              "Self-Attention과 Positional Encoding으로 긴 시퀀스 병렬 처리",
              "장기 의존성과 속도 병목을 해결하는 범용 시퀀스 모델 구조 분석",
            ],
            links: [
              {
                label: "브리프 보기",
                href: "/docs/transformer.pdf",
                note: "public/docs/transformer.pdf 업로드 시 자동 연결됩니다.",
              },
            ],
          },
          {
            title: "BERT & GPT-1/2/3",
            period: "2025.09.15 – 09.19 · 5명",
            bullets: [
              "BERT의 MLM/NSP 프리트레이닝 구조와 파인튜닝 전략 정리",
              "GPT 디코더-온리 아키텍처와 스케일 업 로드맵 비교",
            ],
            links: [
              {
                label: "브리프 보기",
                href: "/docs/bert-gpt.pdf",
                note: "public/docs/bert-gpt.pdf 업로드 시 자동 연결됩니다.",
              },
            ],
          },
          {
            title: "ViT · Swin · Swin v2",
            period: "2025.09.22 – 09.26 · 5명",
            bullets: [
              "ViT 패치 토큰화와 사전학습 전략 정리",
              "Swin Shifted Window, Swin v2 Scaled Cosine Attention 및 상대 위치 바이어스 분석",
            ],
            links: [
              {
                label: "브리프 보기",
                href: "/docs/vit-swin.pdf",
                note: "public/docs/vit-swin.pdf 업로드 시 자동 연결됩니다.",
              },
            ],
          },
          {
            title: "Two-Stage Detector (R-CNN 계열)",
            period: "2025.09.29 – 10.03 · 5명",
            bullets: [
              "R-CNN, Fast/Faster R-CNN, Mask R-CNN 구조와 활용 케이스 비교",
              "Region Proposal 최적화와 멀티태스크 학습 전략 분석",
            ],
            links: [
              {
                label: "브리프 보기",
                href: "/docs/two-stage.pdf",
                note: "public/docs/two-stage.pdf 업로드 시 자동 연결됩니다.",
              },
            ],
          },
          {
            title: "Segment Anything Model 2 (SAM2)",
            period: "2025.10.06 – 10.10 · 5명",
            bullets: [
              "이미지·영상 분할을 위한 Streaming Memory Transformer 구조 탐구",
              "실시간·상호작용 시나리오 최적화 전략 및 데모 구현",
            ],
            links: [
              {
                label: "브리프 보기",
                href: "/docs/sam2.pdf",
                note: "public/docs/sam2.pdf 업로드 시 자동 연결됩니다.",
              },
            ],
          },
          {
            title: "YOLO v1~v5",
            period: "2025.10.13 – 10.17 · 5명",
            bullets: [
              "YOLO 계열 속도·정확도 트레이드오프와 다중 스케일 학습 정리",
              "CSPNet, PANet 등 v5 주요 개선 요소 및 서빙 전략 정리",
            ],
            links: [
              {
                label: "브리프 보기",
                href: "/docs/yolo.pdf",
                note: "public/docs/yolo.pdf 업로드 시 자동 연결됩니다.",
              },
            ],
          },
        ],
      },
      {
        id: "competitions",
        title: "대회 성과 & 수상",
        layout: "grid",
        items: [
          {
            title: "제1회 퀀텀 AI 경진대회",
            highlight: "우수상 · 전주대학교 총장상",
            period: "2025.08",
            bullets: [
              "Fashion-MNIST 양자 분류 과제에서 QNN + CNN 하이브리드 구성",
              "Optuna 기반 하이퍼파라미터 튜닝과 제출 파이프라인 자동화",
            ],
          },
          {
            title: "Toss NEXT ML Challenge – CTR 예측",
            highlight: "20위 / 2,591팀",
            period: "2025.10",
            bullets: [
              "XGBoost·LightGBM·CatBoost 앙상블과 Optuna 기반 AUC-PR 최적화",
              "세션·사용자 집계, 노출/클릭 랙, 타깃 인코딩, 클래스 가중·언더샘플링 전처리",
            ],
          },
          {
            title: "스마트 해운물류 x AI 미션 챌린지",
            highlight: "5위 / 422팀",
            period: "2025.10",
            bullets: [
              "OR-Tools 시간확장 그래프와 Rolling-Horizon으로 AGV 경로 최적화",
              "혼잡 히트맵, 엣지 제약, 시간 슬롯 기반 전처리",
            ],
          },
          {
            title: "동원 x KAIST AI Competition",
            highlight: "68위 / 674팀",
            period: "2025.09",
            bullets: ["현업 데이터 기반의 모델링·피쳐 엔지니어링 실전 수행"],
          },
          {
            title: "2025 금융 AI Challenge",
            highlight: "153위 / 1,070팀",
            period: "2025.08",
            bullets: ["금융 도메인 데이터셋 다루는 AutoML·튜닝 경험 확보"],
          },
          {
            title: "2025 전력사용량 예측 AI",
            highlight: "61위 / 1,613팀",
            period: "2025.08",
            bullets: [
              "LSTM + LightGBM 블렌딩과 SMAPE 커스텀 로스로 에너지 시계열 예측",
              "요일/공휴일/기상 조인과 휴일 이상치 보정 전처리",
            ],
          },
          {
            title: "Boost Up AI 2025 – 신약 개발",
            highlight: "45위 / 1,290팀",
            period: "2025.07",
            bullets: [
              "MPNN·GIN 앙상블과 Optuna 탐색으로 분자 특성 예측",
              "RDKit·SMILES 그래프 파생, Scaffold Split 적용",
            ],
          },
        ],
      },
      {
        id: "value",
        title: "입사 후 기여",
        layout: "cards",
        items: [
          {
            title: "즉시 기여",
            bullets: [
              "전처리 스냅샷·실험 템플릿 표준화(데이터 카드·리포트 자동화)",
              "Optuna + OOF로 재현 가능한 고속 튜닝 파이프라인",
              "FastAPI 배치·캐시, vLLM·ONNX 적용으로 지연·원가 하향",
            ],
          },
          {
            title: "성실 드라이브",
            bullets: [
              "6개월 풀타임 교육 루틴과 리포트 기반 실행력",
              "체력·몰입 루틴으로 야간 대응 가능",
            ],
          },
          {
            title: "장기적 가치",
            bullets: [
              "해외 논문·GitHub 이슈를 빠르게 PoC로 전환",
              "2주 내 최신 논문 구현 및 팀 문서화로 생산성 증대",
            ],
          },
        ],
      },
    ],
    footerNote:
      "논문 브리프·증빙 PDF는 프로젝트 루트의 public/docs 폴더에 업로드하면 /docs/파일명 으로 바로 열 수 있습니다.",
  },
  en: {
    locale: "en",
    hero: {
      name: "Woojin Jang",
      title: "AI Engineer · Full-Stack Builder",
      tagline: "Bridging TensorFlow/PyTorch experimentation with production LLM & RAG services",
      summary:
        "I build reliable LLM and RAG systems that move from notebooks to production. As an Outstanding Trainee in the IBM x Red Hat AI Transformation program, I implemented legal-domain RAG, multi-agent workflows, and Dockerized FastAPI services end to end. Competition results such as Top 20 / 2,591 in Toss NEXT ML Challenge and the Excellence Prize in the Quantum AI Competition prove my delivery focus.",
      highlights: [
        "Transformer / LLM · RAG",
        "Prompt Engineering",
        "MLOps (AWS · Docker · PostgreSQL)",
        "TensorFlow · PyTorch",
      ],
      stats: [
        { label: "Award", value: "Quantum AI Competition – Excellence" },
        { label: "Leaderboard", value: "Toss NEXT ML: 20 / 2,591" },
        { label: "Training", value: "IBM x Red Hat AI Transformation Fellow" },
      ],
      quickFacts: [
        { label: "Email", value: "wjj9319@gmail.com", href: "mailto:wjj9319@gmail.com" },
        { label: "GitHub", value: "github.com/wing0907", href: "https://github.com/wing0907" },
        { label: "LinkedIn", value: "linkedin.com/in/wjinj", href: "https://www.linkedin.com/in/wjinj" },
        { label: "Location", value: "Gwangjin-gu, Seoul, Korea (04996)" },
        { label: "Born", value: "1993 · Male" },
        { label: "Languages", value: "Korean, English (15+ years in Philippines & Canada)" },
      ],
    },
    sections: [
      {
        id: "strengths",
        title: "Core Strengths",
        layout: "bullets",
        items: [
          "Design legal and industry-specific LLM/RAG pipelines with LangChain/LangGraph agents, guardrails, and evidence dashboards",
          "Run reproducible TensorFlow/PyTorch experiments using Optuna, Weights & Biases, K-Fold/OOF, and calibration techniques",
          "Deploy low-latency inference with FastAPI, Docker, AWS (EC2/S3), and Nginx while optimizing cost",
          "Standardize preprocessing snapshots, automated reports, and experiment templates for smoother MLOps",
          "Leverage long-term stays in the Philippines and Canada for fluent English communication and documentation",
        ],
      },
      {
        id: "skills",
        title: "Technical Toolkit",
        layout: "columns",
        columns: [
          {
            title: "Data & Storage",
            items: ["PostgreSQL", "ChromaDB / FAISS", "PyArrow / Parquet", "Pandas"],
          },
          {
            title: "Serving & Backend",
            items: ["FastAPI", "Node.js / Express", "Nginx", "Streamlit"],
          },
          {
            title: "Infra & Ops",
            items: ["Docker", "AWS EC2 / S3", "CUDA", "Linux / Ubuntu"],
          },
          {
            title: "Modeling & Experiments",
            items: ["Optuna", "Weights & Biases", "K-Fold / OOF", "Platt / Isotonic Calibration"],
          },
          {
            title: "Vision & Detection",
            items: ["YOLO family", "ViT / Swin v2", "SAM2", "OpenCV"],
          },
          {
            title: "Collaboration",
            items: ["LangChain / LangGraph", "GitHub", "Slack", "Figma", "VSCode"],
          },
        ],
      },
      {
        id: "experience",
        title: "Experience & Education",
        layout: "stack",
        items: [
          {
            title: "[IBM x Red Hat] AI Transformation",
            subtitle: "Outstanding Trainee · 6-month intensive",
            period: "May 2025 – Nov 2025",
            location: "Korea (hybrid)",
            bullets: [
              "Advanced assignments covering TensorFlow/PyTorch DNN, CNN, RNN, and LLM/RAG agent orchestration",
              "Deployed FastAPI services on Docker & AWS, plus hands-on LangChain/LangGraph, HTML/JavaScript modules",
              "Reproduced AutoEncoder, YOLO, ViT, SAM2, Swin Transformer papers and sharpened prompt engineering",
            ],
          },
          {
            title: "Seneca College – Flight Services (Cabin Operations & Management)",
            subtitle: "Diploma program · GPA 4.0 / 4.0 · Graduate",
            period: "May 2019 – Oct 2020",
            location: "Toronto, Canada",
            bullets: [
              "Served as Amadeus class TA and peer tutor, strengthening leadership and communication",
              "Curriculum on service operations and crisis response improved documentation and playbook design skills",
            ],
          },
          {
            title: "Global Exposure",
            subtitle: "Long-term stays & work in the Philippines and Canada",
            period: "Jan 2003 – Oct 2024",
            location: "Philippines · Canada",
            bullets: [
              "Delivered interpretation for KOTRA events and managed on-site business communication",
              "Worked across F&B, environmental, and construction sectors in multicultural settings",
              "Operate fluently in English and Tagalog for technical papers and collaboration",
            ],
          },
        ],
      },
      {
        id: "projects",
        title: "Flagship Projects",
        layout: "stack",
        items: [
          {
            title: "Team Lemonade LAWAI",
            subtitle: "Legal-domain LLM assistant · 5 members",
            period: "Sep 08 – Nov 07, 2025",
            location: "React · FastAPI · AWS · Docker",
            bullets: [
              "Designed statute & precedent RAG with Llama-3-8B, bge-m3 embeddings, and hybrid Chroma/FAISS/BM25 retrieval",
              "Built LangChain agents (Search, Draft, Critic) with session memory, evidence cards, re-ranking, and dashboards",
              "Deployed FastAPI on Dockerized AWS EC2 and crafted an evidence-first React experience",
            ],
            tags: ["LLM", "RAG", "LangChain", "FastAPI", "Docker", "AWS", "React"],
            links: [
              { label: "Architecture & Gallery", href: "/assets/lawai/gallery.html" },
              { label: "GitHub", href: "https://github.com/wing0907" },
            ],
          },
          {
            title: "Personal Research Repository",
            subtitle: "Transformer · Diffusion · Vision experiments",
            period: "Oct 01 – Oct 20, 2025",
            location: "Solo",
            bullets: [
              "Explored LLM prompt strategies and LangGraph multi-agent scenarios",
              "Documented Transformer, ViT, YOLO reproductions with experiment logs",
              "Shared preprocessing pipelines and automation scripts to speed up team onboarding",
            ],
            tags: ["LLM", "Transformer", "Computer Vision", "LangGraph"],
            links: [{ label: "GitHub Profile", href: "https://github.com/wing0907" }],
          },
        ],
      },
      {
        id: "research",
        title: "Paper Implementation Series",
        layout: "cards",
        items: [
          {
            title: "Transformer Implementation",
            period: "Sep 08 – Sep 12, 2025 · Team of 5",
            bullets: [
              "Parallelized long sequences with self-attention and positional encoding",
              "Analyzed how the architecture resolves long-term dependency bottlenecks",
            ],
            links: [
              {
                label: "View Brief",
                href: "/docs/transformer.pdf",
                note: "Upload transformer.pdf to public/docs to activate the link.",
              },
            ],
          },
          {
            title: "BERT & GPT-1/2/3 Study",
            period: "Sep 15 – Sep 19, 2025 · Team of 5",
            bullets: [
              "Summarized BERT's MLM/NSP pretraining and fine-tuning patterns",
              "Compared decoder-only GPT scaling strategies and next-token objectives",
            ],
            links: [
              {
                label: "View Brief",
                href: "/docs/bert-gpt.pdf",
                note: "Upload bert-gpt.pdf to public/docs to activate the link.",
              },
            ],
          },
          {
            title: "ViT · Swin · Swin v2",
            period: "Sep 22 – Sep 26, 2025 · Team of 5",
            bullets: [
              "Outlined ViT patch tokenization and pretraining tactics",
              "Detailed Swin's shifted windows and Swin v2's scaled cosine attention & relative bias",
            ],
            links: [
              {
                label: "View Brief",
                href: "/docs/vit-swin.pdf",
                note: "Upload vit-swin.pdf to public/docs to activate the link.",
              },
            ],
          },
          {
            title: "Two-Stage Detectors (R-CNN family)",
            period: "Sep 29 – Oct 03, 2025 · Team of 5",
            bullets: [
              "Compared R-CNN, Fast/Faster R-CNN, and Mask R-CNN architectures",
              "Reviewed region proposal optimization and multi-task training tactics",
            ],
            links: [
              {
                label: "View Brief",
                href: "/docs/two-stage.pdf",
                note: "Upload two-stage.pdf to public/docs to activate the link.",
              },
            ],
          },
          {
            title: "Segment Anything Model 2",
            period: "Oct 06 – Oct 10, 2025 · Team of 5",
            bullets: [
              "Explored streaming memory transformer design for image & video segmentation",
              "Implemented real-time, interactive segmentation demos",
            ],
            links: [
              {
                label: "View Brief",
                href: "/docs/sam2.pdf",
                note: "Upload sam2.pdf to public/docs to activate the link.",
              },
            ],
          },
          {
            title: "YOLO v1–v5 Deep Dive",
            period: "Oct 13 – Oct 17, 2025 · Team of 5",
            bullets: [
              "Tracked accuracy/latency trade-offs and multi-scale learning across YOLO versions",
              "Explained CSPNet, PANet, and other v5 enhancements with serving strategies",
            ],
            links: [
              {
                label: "View Brief",
                href: "/docs/yolo.pdf",
                note: "Upload yolo.pdf to public/docs to activate the link.",
              },
            ],
          },
        ],
      },
      {
        id: "competitions",
        title: "Competitions & Awards",
        layout: "grid",
        items: [
          {
            title: "Quantum AI Competition",
            highlight: "Excellence Prize · President of Jeonju University",
            period: "Aug 2025",
            bullets: [
              "Hybrid QNN + CNN solution for Fashion-MNIST quantum classification",
              "Automated submissions with Optuna-driven hyperparameter search",
            ],
          },
          {
            title: "Toss NEXT ML Challenge – CTR",
            highlight: "Rank 20 / 2,591 teams",
            period: "Oct 2025",
            bullets: [
              "Blended XGBoost, LightGBM, CatBoost with Optuna and AUC-PR objective",
              "Engineered session/user aggregates, exposure-click lags, target encoding, and class balancing",
            ],
          },
          {
            title: "Smart Port Logistics x AI Mission Challenge",
            highlight: "Rank 5 / 422 teams",
            period: "Oct 2025",
            bullets: [
              "Optimized AGV routes via OR-Tools time-expanded graphs and rolling horizon control",
              "Built congestion heatmaps, edge constraints, and time-slot preprocessing",
            ],
          },
          {
            title: "Dongwon x KAIST AI Competition",
            highlight: "Rank 68 / 674 teams",
            period: "Sep 2025",
            bullets: ["Delivered end-to-end modeling and feature engineering on real-world datasets"],
          },
          {
            title: "2025 Finance AI Challenge",
            highlight: "Rank 153 / 1,070 teams",
            period: "Aug 2025",
            bullets: ["Gained AutoML and tuning experience on financial datasets"],
          },
          {
            title: "2025 Power Consumption Forecasting",
            highlight: "Rank 61 / 1,613 teams",
            period: "Aug 2025",
            bullets: [
              "Blended LSTM with LightGBM using SMAPE custom loss for energy time-series",
              "Joined calendar/weather features and corrected holiday anomalies",
            ],
          },
          {
            title: "Boost Up AI 2025 – Drug Discovery",
            highlight: "Rank 45 / 1,290 teams",
            period: "Jul 2025",
            bullets: [
              "Built MPNN/GIN ensembles with Optuna search for molecular property prediction",
              "Generated RDKit features, SMILES graphs, and applied scaffold split validation",
            ],
          },
        ],
      },
      {
        id: "value",
        title: "How I Contribute",
        layout: "cards",
        items: [
          {
            title: "Day-1 Impact",
            bullets: [
              "Standardize preprocessing snapshots and experiment templates (data cards, auto reports)",
              "Deliver reproducible hyperparameter pipelines with Optuna + OOF validation",
              "Optimize inference cost with FastAPI batching, caching, and vLLM/ONNX deployment",
            ],
          },
          {
            title: "Drive & Reliability",
            bullets: [
              "Operate with the same full-time cadence proven during the 6-month intensive program",
              "Maintain readiness for late-night support with established focus and stamina routines",
            ],
          },
          {
            title: "Long-Term Value",
            bullets: [
              "Translate new papers and GitHub threads into PoCs within days",
              "Implement and document cutting-edge research within two weeks to uplift team velocity",
            ],
          },
        ],
      },
    ],
    footerNote:
      "Add briefing decks or certificates to public/docs and they will be served automatically from /docs/<filename>.",
  },
};
