# rag/retriever_constitution.py
import argparse, json, re
from pathlib import Path
from collections import Counter
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder

# --- 간단 토크나이저 & 유틸 ---
def normalize_text(s: str) -> str:
    import unicodedata
    if not s: return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("ㆍ","·").replace("ᆞ","·")
    s = re.sub(r"\s+"," ", s).strip()
    return s

KOR_SYNONYM_MAP = {
    "재선":"중임","연임":"중임",
    "몇년":"임기","몇 년":"임기",
    "직무대행":"권한대행",
    "수정헌법":"헌법개정",
    "국민투표법":"국민투표",
}
def expand_synonyms(q: str) -> str:
    qn = normalize_text(q)
    for k,v in KOR_SYNONYM_MAP.items():
        qn = qn.replace(k, v)
    qn = re.sub(r"제\s*(\d+)\s*조", r"제\1조", qn)
    qn = re.sub(r"(\d+)\s*조", r"제\1조", qn)
    return qn

CIRCLE_MAP = dict(zip("①②③④⑤⑥⑦⑧⑨⑩",[str(i) for i in range(1,11)]))
ART_RE  = re.compile(r"제?\s*(\d+)\s*조")
PARA_RE = re.compile(r"제?\s*([0-9①-⑩]+)\s*항")
def extract_refs(q: str):
    qn = normalize_text(q)
    for k,v in CIRCLE_MAP.items(): qn = qn.replace(k,v)
    arts = [int(x) for x in ART_RE.findall(qn)]
    paras= [int(x) for x in PARA_RE.findall(qn) if str(x).isdigit()]
    return {"articles":arts, "paras":paras}

def ko_tokens(s: str):
    s = normalize_text(s)
    words = re.findall(r"[가-힣A-Za-z0-9]+", s)
    bigr=[]
    for w in words:
        if re.search(r"[가-힣]", w) and len(w)>=2:
            bigr += [w[i:i+2] for i in range(len(w)-1)]
    return words + bigr

# --- 경로 ---
ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "index" / "constitution"
META_PATH = INDEX_DIR / "meta.jsonl"
FAISS_PATH= INDEX_DIR / "faiss.index"
EMB_MODEL= "BAAI/bge-m3"
RERANKER = "BAAI/bge-reranker-base"   # 속도/정확도 균형

# --- 데이터 로드 ---
def load_meta(p: Path):
    rows=[]
    with open(p,"r",encoding="utf-8") as f:
        for line in f:
            s=line.strip()
            if s: rows.append(json.loads(s))
    return rows

# --- BM25 (rank_bm25가 있으면 사용) ---
try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None

class SparseBM25:
    def __init__(self, docs):
        self.docs = docs
        if BM25Okapi:
            self.tokens = [ko_tokens(d) for d in docs]
            self.engine = BM25Okapi(self.tokens)
        else:
            # 매우 단순한 TF-IDF식 대체 (소형 코퍼스용)
            from math import log
            self.tokens = [ko_tokens(d) for d in docs]
            self.df={}
            for toks in self.tokens:
                for t in set(toks):
                    self.df[t]=self.df.get(t,0)+1
            self.N=len(self.tokens)
            self.idf={t: np.log((self.N+1)/(df+1))+1 for t,df in self.df.items()}
    def search(self, q, topn=50):
        qt = ko_tokens(q)
        if BM25Okapi:
            scores = self.engine.get_scores(qt)
        else:
            # 간이 가중치: sum(tf * idf)
            scores=[]
            for toks in self.tokens:
                tf = Counter(toks)
                s = sum(tf[t]*self.idf.get(t,0.0) for t in set(qt))
                scores.append(s)
        idx = np.argsort(scores)[::-1][:topn]
        return np.array(scores)[idx], idx

# --- 메인 ---
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q","--query", required=True)
    ap.add_argument("--topk", type=int, default=4)
    ap.add_argument("--pool", type=int, default=60, help="후보 수집 개수")
    ap.add_argument("--max_chars", type=int, default=1600)
    args = ap.parse_args()

    meta = load_meta(META_PATH)
    index = faiss.read_index(str(FAISS_PATH))
    dense = SentenceTransformer(EMB_MODEL, device="cuda" if faiss.get_num_gpus()>0 else "cpu")

    # sparse 준비
    corpus_texts = [ (m.get("text") or "")[:1500] for m in meta ]
    bm25 = SparseBM25(corpus_texts)

    # 질의 전처리/확장 (질문이 다양해도 커버)
    q_raw  = args.query
    q1 = normalize_text(q_raw)
    q2 = expand_synonyms(q_raw)
    q3 = q2.replace("은 뭐야","는 무엇인가").replace("뭐임","무엇인가")
    queries = list(dict.fromkeys([q_raw,q1,q2,q3]))  # 중복 제거
    refs = extract_refs(q2)

    # 1) Dense 후보 모으기 (여러 reformulation 앙상블)
    cand_idx=set(); dense_scores={}
    for q in queries:
        qv = dense.encode([q], normalize_embeddings=True)
        D, I = index.search(qv, args.pool//len(queries)+5)
        for s, i in zip(D[0], I[0]):
            cand_idx.add(int(i))
            dense_scores[int(i)] = max(dense_scores.get(int(i), -1e9), float(s))

    # 2) Sparse 후보 추가
    s_scores, s_idx = bm25.search(q2, topn=args.pool)
    for s, i in zip(s_scores, s_idx):
        cand_idx.add(int(i))

    cands = []
    for i in cand_idx:
        it = meta[i].copy()
        it["_dense"] = dense_scores.get(i, 0.0)
        # 간이 sparse 점수
        it["_sparse"] = float(s_scores[list(s_idx).index(i)]) if i in s_idx else 0.0
        cands.append(it)

    # 3) 규칙 가중치 (조/항/단위 일치시 가점, 구조 단위 가감)
    def rule_boost(item):
        w=0.0
        unit=item.get("unit","")
        if unit in ("조문","항","호","목"): w+=0.5
        if unit in ("장","전문","부칙"):     w-=0.3
        art=item.get("article_no")
        if art and str(art).isdigit() and refs["articles"] and int(art) in refs["articles"]:
            w+=0.8
        if refs["paras"]:
            tail=item.get("id","").split("::",1)[-1]
            if any(str(p) in tail for p in refs["paras"]): w+=0.4
        return w
    for c in cands:
        c["_rule"]=rule_boost(c)

    # 4) Cross-Encoder 재랭크
    rer = CrossEncoder(RERANKER, device="cuda" if faiss.get_num_gpus()>0 else "cpu")
    pairs=[(q2, (c.get("text") or "")[:1024]) for c in cands]
    rscore = rer.predict(pairs)
    for c,s in zip(cands, rscore):
        c["_rerank"]=float(s)

    # 5) 최종 점수 (가중치 앙상블) — 질문이 다양해도 일관
    for c in cands:
        c["_final"] = 0.6*c["_rerank"] + 0.2*c["_dense"] + 0.15*c["_sparse"] + 0.05*c["_rule"]
    cands.sort(key=lambda x: x["_final"], reverse=True)

    # 6) 모드 판별: “어디/몇조/근거” → reference 우선
    q_mode = "locate" if any(w in q_raw for w in ["어디","몇조","근거","조문","항","헌법 제"]) else "answer"

    # 7) 기사(조) 단위 일관성 유지: 같은 조가 많이 뽑히면 그 조 위주로
    topN = cands[:max(args.topk*2, 6)]
    cnt = Counter([c.get("article_no") for c in topN if c.get("article_no")])
    main_art = cnt.most_common(1)[0][0] if cnt else None
    picked=[]
    for c in cands:
        if q_mode=="locate" and main_art and c.get("article_no")!=main_art: 
            continue
        picked.append(c)
        if len(picked)>=args.topk: break

    # 8) 컨텍스트 구성
    ctx=[]; total=0
    for c in picked:
        t=(c.get("text") or "").strip()
        if not t: continue
        head=[]
        if c.get("article_no"): head.append(f"제{c['article_no']}조")
        if c.get("unit") in {"항","호","목"} and "::" in c["id"]:
            head.append(c["id"].split("::",1)[1])
        title=" ".join(head) if head else c.get("unit","")
        block=f"[{title}] {t}" if title else t
        if total+len(block)>args.max_chars: break
        ctx.append(block); total+=len(block)

    print("\n=== CONTEXT ===\n" + "\n\n".join(ctx))

if __name__ == "__main__":
    main()