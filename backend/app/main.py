"""
FastAPI 애플리케이션 정의
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# 데이터베이스 초기화 함수
def init_db():
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("데이터베이스 테이블이 성공적으로 생성되었습니다.")
    except Exception as e:
        logger.error(f"데이터베이스 초기화 중 오류 발생: {str(e)}")
        raise

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Org-mode 기반 클라우드 노트 서비스 API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("애플리케이션이 시작되었습니다.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("애플리케이션이 종료됩니다.")

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "healthy"} 