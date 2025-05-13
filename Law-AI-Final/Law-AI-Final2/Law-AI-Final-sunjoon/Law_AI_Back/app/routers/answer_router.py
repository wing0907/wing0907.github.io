import os
from dotenv import load_dotenv
from typing import List
from typing_extensions import TypedDict
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

# LangChain 및 LangGraph 관련 라이브러리 임포트
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END


# --- 환경 변수 로드 ---
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY 환경 변수를 설정해주세요.")


# --- Pydantic 모델 정의 ---
class QueryRequest(BaseModel):
    query: str
    no_llm: bool = False

class RetrievalItem(BaseModel):
    content: str
    source: str

class AnswerResponse(BaseModel):
    answer: str
    retrieval: List[RetrievalItem]


# --- LangGraph 상태(State) 정의 ---
class GraphState(TypedDict):
    """
    LangGraph의 전체 흐름에서 관리될 데이터의 형태(schema)를 정의합니다.

    Attributes:
        question: 사용자의 원본 질문
        rewritten_question: 검색에 사용하기 위해 재구성된 질문
        documents: Retriever를 통해 검색된 문서 리스트
        grade: 검색된 문서가 질문과 관련이 있는지 평가한 결과
        generation: LLM이 생성한 최종 답변
    """
    question: str
    rewritten_question: str
    documents: List[Document]
    grade: str
    generation: str


# --- RAG 파이프라인 구성 요소 ---

# 1. 임베딩 모델 및 ChromaDB 로드
print("임베딩 모델(BAAI/bge-m3)을 로드하는 중입니다...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={'device': 'cpu'}, # GPU 사용 시 'cuda'로 변경
    encode_kwargs={'normalize_embeddings': True}
)

db_path = Path(__file__).resolve().parents[3] / "Law_AI_DB" / "data"
if not db_path.exists():
    raise FileNotFoundError(f"ChromaDB 경로를 찾을 수 없습니다: {db_path}")

print(f"ChromaDB를 로드하는 중입니다... 경로: {db_path}")
vectorstore = Chroma(
    persist_directory=str(db_path), 
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
print("임베딩 모델 및 ChromaDB 로드 완료.")


# 2. LLM 모델 및 파이프라인 체인(Chain) 정의
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

# 2-1. 쿼리 재구성기 (Query Rewriter)
rewrite_prompt = PromptTemplate(
    template="""
    ## 지시사항
    당신은 벡터 검색을 위한 검색어 생성 전문가입니다.
    사용자의 질문을 분석하여, 관련 문서를 가장 잘 찾을 수 있는 간결하고 핵심적인 검색어로 재구성해주세요.
    다른 설명 없이, 재구성된 검색어만 출력해야 합니다.

    ## 사용자 질문
    {question}

    ## 쿼리 예시

    """,
    input_variables=["question"],
)
query_rewriter = rewrite_prompt | llm | StrOutputParser()

# 2-2. 문서 채점기 (Document Grader)
grading_prompt = PromptTemplate(
    template="""
    ## 지시사항
    주어진 정보가 사용자의 질문에 대한 답변과 관련이 있는지 평가하세요.
    
    ## 정보
    {document}
    
    ## 사용자 질문
    {question}
    
    ## 평가
    정보가 질문과 관련이 있다면 'yes', 관련이 없다면 'no'를 `binary_score` 키의 값으로 하는 JSON 객체를 반환하세요.
    
    ## 출력 예시
    {{"binary_score": "yes"}}
    """,
    input_variables=["document", "question"],
)
grader = grading_prompt | llm | JsonOutputParser()

# 2-3. 답변 생성기 (Response Generator)
generation_prompt = PromptTemplate(
    template="""
    ## 지시사항
    당신은 법률 자문을 제공하는 AI 어시스턴트입니다.
    주어진 정보(문서)를 바탕으로 사용자의 질문에 대해 명확하고 이해하기 쉽게 한국어로 답변해주세요.
    정보에 질문과 관련된 내용이 없다면, 아는 내용을 바탕으로 답변하지 말고 정보가 부족하다고 솔직하게 답변하세요.

    ## 정보 (문서)
    {documents}

    ## 사용자 질문
    {question}
    """,
    input_variables=["documents", "question"],
)
generator = generation_prompt | llm | StrOutputParser()


# --- LangGraph 노드(Node) 함수 정의 ---

def rewrite_query(state: GraphState):
    """사용자의 질문을 검색에 용이한 키워드로 재구성하는 노드"""
    print("--- 노드 실행: rewrite_query ---")
    question = state["question"]
    rewritten_question = query_rewriter.invoke({"question": question})
    print(f"원본 쿼리: '{question}'")
    print(f"재구성된 쿼리: '{rewritten_question}'")
    state["rewritten_question"] = rewritten_question
    return state

def retrieve(state: GraphState):
    """재구성된 쿼리를 사용해 문서를 검색하는 노드"""
    print("--- 노드 실행: retrieve ---")
    rewritten_question = state["rewritten_question"]
    documents = retriever.invoke(rewritten_question)
    state["documents"] = documents
    return state

def grade_documents(state: GraphState):
    """검색된 문서가 원본 질문과 관련이 있는지 평가하는 노드"""
    print("--- 노드 실행: grade_documents ---")
    question = state["question"]
    documents = state["documents"]
    
    relevant_docs = []
    for doc in documents:
        result = grader.invoke({"document": doc.page_content, "question": question})
        if result.get("binary_score", "no").lower() == "yes":
            relevant_docs.append(doc)
            
    if relevant_docs:
        print(f"평가 결과: 관련성 있는 문서 {len(relevant_docs)}개 발견")
        state["grade"] = "relevant"
        state["documents"] = relevant_docs
    else:
        print("평가 결과: 관련성 있는 문서 없음")
        state["grade"] = "not_relevant"
        state["documents"] = []
        
    return state

def generate(state: GraphState):
    """관련성 있는 문서를 바탕으로 최종 답변을 생성하는 노드"""
    print("--- 노드 실행: generate ---")
    question = state["question"]
    documents = state["documents"]
    generation = generator.invoke({"documents": documents, "question": question})
    state["generation"] = generation
    return state
    
def fallback(state: GraphState):
    """관련 문서를 찾지 못했을 때 대체 답변을 제공하는 노드"""
    print("--- 노드 실행: fallback ---")
    state["generation"] = "죄송합니다, 질문에 답변할 수 있는 관련 정보를 찾지 못했습니다. 질문을 더 구체적으로 작성해주시면 좋습니다."
    return state


# --- LangGraph 그래프 생성 및 엣지(Edge) 연결 ---
workflow = StateGraph(GraphState)

# 노드 추가
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("fallback", fallback)

# 엣지 연결
workflow.set_entry_point("rewrite_query")
workflow.add_edge("rewrite_query", "retrieve")
workflow.add_edge("retrieve", "grade_documents")

workflow.add_conditional_edges(
    "grade_documents",
    lambda state: state["grade"],
    {
        "relevant": "generate",
        "not_relevant": "fallback"
    }
)
workflow.add_edge("generate", END)
workflow.add_edge("fallback", END)

# 그래프 컴파일
rag_app = workflow.compile()


# --- FastAPI 라우터 설정 ---
router = APIRouter()

@router.post("/answer", response_model=AnswerResponse)
async def get_answer(request: QueryRequest):
    """
    LangGraph RAG 파이프라인을 사용하여 답변을 생성하는 API
    """
    inputs = {"question": request.query}
    final_state = rag_app.invoke(inputs)

    answer = final_state.get("generation", "오류: 답변을 생성하지 못했습니다.")
    retrieval_docs = []
    if final_state.get("documents"):
        for doc in final_state["documents"]:
            retrieval_docs.append(
                RetrievalItem(content=doc.page_content, source=doc.metadata.get("source", "출처 없음"))
            )

    return AnswerResponse(answer=answer, retrieval=retrieval_docs)