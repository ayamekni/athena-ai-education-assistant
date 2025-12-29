"""
ATHENA RAG Router - AI Assistant endpoints with GPU support
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List

from app.services.model_loader import get_answer_with_sources, rag_chain
from app.core.security import get_current_user

router = APIRouter(prefix="/athena", tags=["ATHENA AI Assistant"])


class QuestionRequest(BaseModel):
    """Request schema for asking questions"""
    question: str = Field(..., min_length=3, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is machine learning?"
            }
        }


class AnswerResponse(BaseModel):
    """Response schema with answer and sources"""
    answer: str
    sources: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "🌟 Introduction\nMachine Learning is...",
                "sources": [
                    "Machine Learning is a subset of AI...",
                    "ML algorithms learn from data..."
                ]
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    gpu_available: bool
    components: dict


@router.get("/ask", response_model=AnswerResponse)
async def ask_athena(
    question: str = Query(..., min_length=3, max_length=500),
    current_user: dict = Depends(get_current_user)
):
    """
    Ask ATHENA a question (GET endpoint with query parameter)
    
    Returns answer with source chunks used for generation.
    """
    try:
        answer, sources = get_answer_with_sources(question)
        return AnswerResponse(answer=answer, sources=sources)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}"
        )


@router.post("/ask", response_model=AnswerResponse)
async def ask_athena_post(
    request: QuestionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Ask ATHENA a question (POST endpoint with JSON body)
    
    Returns answer with source chunks used for generation.
    """
    try:
        answer, sources = get_answer_with_sources(request.question)
        return AnswerResponse(answer=answer, sources=sources)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def athena_health():
    """
    Check ATHENA system health and component status
    
    No authentication required.
    """
    import torch
    
    try:
        chain_fn, retriever = rag_chain()
        
        return HealthResponse(
            status="healthy",
            gpu_available=torch.cuda.is_available(),
            components={
                "vectorstore": "loaded",
                "llm": "loaded",
                "rag_chain": "ready",
                "device": "cuda" if torch.cuda.is_available() else "cpu"
            }
        )
    except Exception as e:
        return HealthResponse(
            status="degraded",
            gpu_available=torch.cuda.is_available(),
            components={
                "error": str(e),
                "device": "cuda" if torch.cuda.is_available() else "cpu"
            }
        )
