// src/api/askBackend.ts

// 1. API 응답의 타입을 정의하는 인터페이스를 export 합니다.
export interface BackendResponse {
  answer: string;
  retrieval?: Record<string, any>[]; // retrieval은 객체들의 배열
}

// 2. 함수의 반환 값으로 Promise<BackendResponse>를 명시합니다.
export async function askBackend(query: string, noLLM = false): Promise<BackendResponse> {
  const res = await fetch("/api/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, no_llm: noLLM }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`HTTP ${res.status}: ${err}`);
  }
  // res.json()이 위에서 정의한 BackendResponse 타입의 Promise를 반환할 것이라고 명시
  return res.json();
}