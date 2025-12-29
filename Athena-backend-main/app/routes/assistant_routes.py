"""
ATHENA Assistant Routes
API endpoints for the AI assistant - STATELESS (No conversation persistence)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.assistant_schema import (
    QuestionRequest, 
    AnswerResponse,
    QuizRequest,
    QuizResponse,
    QuizGradingRequest,
    QuizGradingResponse,
    QuestionReview,
    StudentAnswer
)
from app.services.rag_service import generate_athena_answer, get_last_context
from app.services.quiz_generator import generate_quiz
from app.core.security import require_role
from typing import Dict

router = APIRouter(
    prefix="/assistant",
    tags=["ATHENA Assistant"]
)

# Store for quiz data (in-memory for now - maps quiz_id to quiz data)
_quiz_store: Dict[str, dict] = {}


@router.post("/ask", response_model=AnswerResponse, status_code=status.HTTP_200_OK)
async def ask_athena(
    request: QuestionRequest,
    current_user=Depends(require_role(["student", "teacher"]))
):
    """
    Ask ATHENA a question and get an AI-generated answer
    
    STATELESS MODE: No conversation history is saved.
    Each request is independent and uses only RAG context.
    
    The assistant uses RAG (Retrieval-Augmented Generation) with:
    - FAISS vector store for context retrieval
    - TinyLlama LLM for answer generation (GPU-accelerated)
    - Educational prompt engineering for clear, structured responses
    
    Args:
        request: QuestionRequest with the student's question
        current_user: Authenticated user (student or teacher)
        
    Returns:
        AnswerResponse with ATHENA's generated answer and context used
        
    Raises:
        HTTPException: If answer generation fails
    """
    try:
        # ✅ Generate answer using RAG service (FAISS + ATHENA prompt + LLM)
        answer = await generate_athena_answer(request.question)
        
        # Get context that was used for this answer
        context_used = get_last_context()
        
        # ✅ Return simple response - NO conversation saving
        return AnswerResponse(
            answer=answer,
            context_used=context_used if context_used else "No specific context used"
        )
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"ATHENA knowledge base not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate answer: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def assistant_health():
    """
    Check if ATHENA assistant is ready
    
    Returns:
        Status of the AI assistant components
    """
    from app.services.rag_service import vectorstore, llm, rag_chain
    
    return {
        "status": "operational" if all([vectorstore, llm, rag_chain]) else "initializing",
        "components": {
            "vectorstore": "loaded" if vectorstore is not None else "not loaded",
            "llm": "loaded" if llm is not None else "not loaded",
            "rag_chain": "loaded" if rag_chain is not None else "not loaded"
        }
    }


# ==================== QUIZ ENDPOINTS ====================

@router.post("/quiz", response_model=QuizResponse, status_code=status.HTTP_200_OK)
async def generate_quiz_endpoint(
    request: QuizRequest,
    current_user=Depends(require_role(["student", "teacher"]))
):
    """
    Generate a quiz on a specific topic
    
    Supported topics:
    - Python
    - Machine Learning
    - Deep Learning
    - NLP (Natural Language Processing)
    - Computer Vision
    
    Args:
        request: QuizRequest with topic, number of questions, and difficulty
        current_user: Authenticated user
        
    Returns:
        QuizResponse with generated quiz questions
        
    Raises:
        HTTPException: If quiz generation fails or topic is not supported
    """
    try:
        # Generate quiz using static data generator
        quiz = generate_quiz(
            topic=request.topic,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
        
        # Store quiz data for later grading
        _quiz_store[quiz.quiz_id] = {
            "quiz": quiz,
            "topic": quiz.topic,
            "num_questions": quiz.num_questions,
            "questions": [q.to_dict() for q in quiz.questions]
        }
        
        # Return quiz response
        return QuizResponse(
            quiz_id=quiz.quiz_id,
            topic=quiz.topic,
            num_questions=quiz.num_questions,
            questions=[
                {
                    "question_id": q.question_id,
                    "question_text": q.question_text,
                    "options": q.options,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                    "difficulty": q.difficulty
                }
                for q in quiz.questions
            ],
            formatted_display=quiz.formatted_display,
            context_used=quiz.context_used
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid quiz topic: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )


@router.post("/quiz/{quiz_id}/grade", response_model=QuizGradingResponse, status_code=status.HTTP_200_OK)
async def grade_quiz_endpoint(
    quiz_id: str,
    request: QuizGradingRequest,
    current_user=Depends(require_role(["student", "teacher"]))
):
    """
    Grade a quiz and return results with explanations
    
    Args:
        quiz_id: ID of the quiz to grade
        request: QuizGradingRequest with student answers
        current_user: Authenticated user
        
    Returns:
        QuizGradingResponse with score and answer review
        
    Raises:
        HTTPException: If quiz not found or grading fails
    """
    try:
        # Retrieve quiz data
        if quiz_id not in _quiz_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz with ID {quiz_id} not found"
            )
        
        stored_quiz = _quiz_store[quiz_id]
        quiz_questions = stored_quiz["questions"]
        topic = stored_quiz["topic"]
        
        # Create a map of question_id to question data
        questions_map = {q["question_id"]: q for q in quiz_questions}
        
        # Grade the quiz
        correct_count = 0
        answers_review = []
        
        for answer in request.answers:
            question_id = answer.question_id
            student_answer = answer.student_answer
            
            if question_id not in questions_map:
                continue
            
            question = questions_map[question_id]
            correct_answer = question["correct_answer"]
            is_correct = student_answer.strip().lower() == correct_answer.strip().lower()
            
            if is_correct:
                correct_count += 1
            
            answers_review.append(
                QuestionReview(
                    question_id=question_id,
                    question_text=question["question_text"],
                    student_answer=student_answer,
                    correct_answer=correct_answer,
                    is_correct=is_correct,
                    explanation=question["explanation"],
                    difficulty=question["difficulty"]
                )
            )
        
        # Calculate score
        total_questions = len(quiz_questions)
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        return QuizGradingResponse(
            quiz_id=quiz_id,
            topic=topic,
            total_questions=total_questions,
            correct_answers=correct_count,
            score_percentage=score_percentage,
            answers_review=answers_review
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to grade quiz: {str(e)}"
        )
