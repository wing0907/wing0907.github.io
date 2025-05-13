from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import answer_router, auth_router
from . import database
from . import models

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 프론트엔드 개발 서버의 주소를 origins에 추가해야 합니다.
origins = [
    "http://localhost:5173",      # Vite 로컬 개발 서버 주소
    "http://127.0.0.1:5173", # Vite 네트워크 개발 서버 주소
]

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 허용할 출처
    allow_credentials=True,      # 쿠키 허용
    allow_methods=["*"],         # 모든 HTTP 메소드 허용
    allow_headers=["*"],         # 모든 HTTP 헤더 허용
)

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)
    print("Database connected and tables verified.")


# 라우터들을 앱에 포함시킵니다.
app.include_router(answer_router.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api/auth")

# 서버 상태 확인을 위한 루트 경로
@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI 백엔드 서버가 정상적으로 실행 중입니다."}
