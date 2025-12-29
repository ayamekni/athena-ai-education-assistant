"""
ATHENA Assistant Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List


class QuestionRequest(BaseModel):
    """Request schema for asking ATHENA a question"""
    question: str = Field(..., min_length=1, max_length=1000, description="The question to ask ATHENA")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is machine learning?"
                }
            ]
        }
    }


class AnswerResponse(BaseModel):
    """Response schema for ATHENA's answer - STATELESS"""
    answer: str = Field(..., description="ATHENA's generated answer")
    context_used: str = Field(..., description="Context retrieved from FAISS for this answer")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "Machine learning is a subset of artificial intelligence...",
                    "context_used": "Course material on AI fundamentals"
                }
            ]
        }
    }


# ==================== QUIZ SCHEMAS ====================

class QuizQuestion(BaseModel):
    """Schema for a single quiz question"""
    question_id: int = Field(..., description="Unique ID for this question")
    question_text: str = Field(..., description="The question text")
    options: List[str] = Field(..., description="List of answer options")
    correct_answer: str = Field(..., description="The correct answer text")
    explanation: str = Field(..., description="Explanation for the correct answer")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")


class QuizResponse(BaseModel):
    """Response schema for a generated quiz"""
    quiz_id: str = Field(..., description="Unique ID for this quiz")
    topic: str = Field(..., description="The quiz topic")
    num_questions: int = Field(..., description="Number of questions in the quiz")
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")
    formatted_display: str = Field(..., description="Formatted string representation of the quiz")
    context_used: str = Field(..., description="Source of the quiz questions")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "quiz_id": "uuid-string",
                    "topic": "Python",
                    "num_questions": 5,
                    "questions": [
                        {
                            "question_id": 1,
                            "question_text": "What is Python?",
                            "options": ["A snake", "A programming language", "A brand"],
                            "correct_answer": "A programming language",
                            "explanation": "Python is a high-level programming language",
                            "difficulty": "easy"
                        }
                    ],
                    "formatted_display": "# Python Quiz...",
                    "context_used": "Static Quiz Generator"
                }
            ]
        }
    }


class QuizRequest(BaseModel):
    """Request schema for generating a quiz"""
    topic: str = Field(..., min_length=1, description="Quiz topic (python, machine learning, deep learning, nlp, computer vision)")
    num_questions: int = Field(default=10, ge=1, le=50, description="Number of questions (1-50)")
    difficulty: str = Field(default="mixed", description="Difficulty level: easy, medium, hard, or mixed")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "topic": "Python",
                    "num_questions": 10,
                    "difficulty": "mixed"
                }
            ]
        }
    }


class StudentAnswer(BaseModel):
    """Schema for a student's answer to a quiz question"""
    question_id: int = Field(..., description="ID of the question being answered")
    student_answer: str = Field(..., description="The answer provided by the student")


class QuizGradingRequest(BaseModel):
    """Request schema for grading a quiz"""
    quiz_id: str = Field(..., description="ID of the quiz being graded")
    answers: List[StudentAnswer] = Field(..., description="List of student answers")


class QuestionReview(BaseModel):
    """Schema for reviewing a single graded question"""
    question_id: int
    question_text: str
    student_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    difficulty: str


class QuizGradingResponse(BaseModel):
    """Response schema for quiz grading results"""
    quiz_id: str = Field(..., description="ID of the graded quiz")
    topic: str = Field(..., description="Quiz topic")
    total_questions: int = Field(..., description="Total number of questions")
    correct_answers: int = Field(..., description="Number of correct answers")
    score_percentage: float = Field(..., description="Score as a percentage (0-100)")
    answers_review: List[QuestionReview] = Field(..., description="Review of each answer")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "quiz_id": "uuid-string",
                    "topic": "Python",
                    "total_questions": 5,
                    "correct_answers": 4,
                    "score_percentage": 80.0,
                    "answers_review": [
                        {
                            "question_id": 1,
                            "question_text": "What is Python?",
                            "student_answer": "A programming language",
                            "correct_answer": "A programming language",
                            "is_correct": True,
                            "explanation": "Correct! Python is a high-level programming language",
                            "difficulty": "easy"
                        }
                    ]
                }
            ]
        }
    }
