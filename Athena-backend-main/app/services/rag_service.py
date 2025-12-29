"""
ATHENA RAG Service - AI Assistant with FAISS Vector Store and Mistral-7B
Optimized for GTX 1650 (4GB VRAM) using 4-bit quantization
"""
import os
import re
import pickle
import torch
from typing import List
from pathlib import Path

# Check GPU availability
if torch.cuda.is_available():
    print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
    print(f"✅ VRAM available: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
else:
    print("⚠️ Running ATHENA on CPU — will be VERY slow")

# LangChain imports
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

# Transformers imports
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline
)

# Configuration
FAISS_INDEX_PATH = "athena_faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Using TinyLlama (1.1GB) - smallest fast model for quick testing
LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Global variables for loaded models
vectorstore = None
llm = None
rag_chain = None
last_context = None  # Track last retrieved context for API response


def get_last_context() -> str:
    """Get the last context retrieved from FAISS"""
    global last_context
    return last_context if last_context else "No context retrieved"


def load_faiss_index():
    """Load FAISS vector store from disk"""
    global vectorstore
    
    print("\n🔄 Loading FAISS index...")
    
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Load FAISS index
    index_path = Path(FAISS_INDEX_PATH)
    if not index_path.exists():
        raise FileNotFoundError(
            f"❌ FAISS index not found at {FAISS_INDEX_PATH}\n"
            f"Please ensure the following files exist:\n"
            f"  - {FAISS_INDEX_PATH}/index.faiss\n"
            f"  - {FAISS_INDEX_PATH}/index.pkl"
        )
    
    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    print(f"✅ FAISS index loaded successfully")
    return vectorstore


def load_mistral_model():
    """Load Phi-2 with 4-bit quantization - smaller and faster"""
    global llm
    
    print(f"\n🔄 Loading {LLM_MODEL} with 4-bit quantization...")
    
    # 4-bit quantization config for low VRAM
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        LLM_MODEL,
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with 4-bit quantization
    model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL,
        quantization_config=quant_config,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )
    
    # Create text generation pipeline with strict limits
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=250,  # ✅ Cap response length to prevent rambling
        temperature=0.5,      # ✅ Lower temperature for more focused answers
        top_p=0.9,
        repetition_penalty=1.2,
        do_sample=True,
        return_full_text=False
    )
    
    # Wrap in LangChain HuggingFacePipeline
    llm = HuggingFacePipeline(pipeline=pipe)
    
    print(f"✅ {LLM_MODEL} loaded successfully with 4-bit quantization")
    return llm


def combine_docs(docs: List[Document]) -> str:
    """
    Combine retrieved documents into context string
    
    If no documents are found, returns minimal fallback to prevent hallucinations.
    """
    if not docs:
        # ✅ Minimal fallback - prevents generic chatbot behavior
        return "No FAISS context available. Provide a short, clear educational explanation."
    
    context_parts = []
    for i, doc in enumerate(docs, 1):
        content = doc.page_content.strip()
        if content:  # Only add non-empty content
            context_parts.append(content)
    
    if not context_parts:
        return "No FAISS context available. Provide a short, clear educational explanation."
    
    # Return just the content, no fancy formatting
    return "\n\n".join(context_parts)


def build_rag_chain():
    """Build the complete RAG chain with FAISS retriever and Mistral-7B"""
    global rag_chain
    
    print("\n🔄 Building RAG chain...")
    
    # Create retriever from FAISS vectorstore
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # ✅ PROFESSIONAL ATHENA SYSTEM PROMPT - OPTIMIZED FOR FRONTEND DISPLAY
    prompt_template = """You are ATHENA — the professional AI academic mentor for ESPRIM students.

YOUR ROLE:
- Deliver clear, structured educational answers
- Support student learning with evidence-based explanations
- Maintain academic integrity and professionalism
- Format responses for optimal readability

RESPONSE STRUCTURE:
For CONCEPTUAL questions:
1. Clear Definition (1-2 sentences)
2. Key Components (use • bullets)
3. Practical Example (if helpful)
4. Why It Matters (context and relevance)

For CODE/ALGORITHM questions:
1. Explanation (what it does)
2. Step-by-Step Breakdown (numbered)
3. Code Example (if applicable)
4. Common Use Cases

For COMPARISON questions:
1. Item A Overview
2. Item B Overview
3. Key Differences (use comparison format)
4. When to Use Each

For WHY questions:
1. Direct Answer
2. Underlying Principles
3. Historical/Technical Context
4. Real-World Application

FORMATTING RULES:
- Use clear section headers with consistent formatting
- Use bullet points (•) for lists
- Use numbered lists (1., 2., 3.) for sequences
- Use **bold** for key terms only
- Keep paragraphs short (2-3 sentences max)
- Avoid excessive punctuation or emojis
- Use code blocks for technical content: ```code```

QUALITY STANDARDS:
- Be precise and academically rigorous
- Support claims with evidence from course materials
- Avoid speculation or unsupported statements
- Provide complete answers without asking "would you like to know more?"
- Never use filler phrases or generic openings

CONTENT GUIDELINES:
- Use beginner-friendly language for complex topics
- Define unfamiliar terms on first mention
- Build from basic to advanced concepts
- Connect new information to prior knowledge
- Provide actionable insights

Course Materials:
{context}

Student Question:
{question}

Your professional, well-structured answer:"""
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Build RAG chain
    rag_chain = (
        {
            "context": retriever | combine_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )
    
    print("✅ RAG chain built successfully")
    return rag_chain


def clean_output(text: str) -> str:
    """
    Clean and format LLM output for professional display
    Preserves structure while removing artifacts
    """
    text = text.strip()
    
    # ✅ Remove common unwanted patterns and artifacts
    unwanted_patterns = [
        r"^Your Answer:[\s]*",
        r"^Answer:[\s]*",
        r"^ATHENA:[\s]*",
        r"^Assistant:[\s]*",
        r"^Student:[\s]*",
        r"^Question:[\s]*",
        r"\[your name here\]",
        r"\[insert .*?\]",
        r"What would you like.*?\?",
        r"Would you like to.*?\?",
        r"Do you have any.*?\?",
        r"Feel free to ask.*?\.",
        r"Is there anything.*?\?",
        r"^Study tip:.*$",
        r"^Here is another.*$",
        r"^ATHENA continues.*$",
        r"</s>",
        r"<s>",
        r"<\|im_end\|>",
        r"<\|im_start\|>.*?\n",
    ]
    
    for pattern in unwanted_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove duplicate consecutive newlines (but preserve intentional spacing)
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Remove leading/trailing whitespace from each line
    lines = text.split("\n")
    lines = [line.rstrip() for line in lines]
    text = "\n".join(lines).strip()
    
    # Remove duplicate sentences/content
    lines = text.split("\n")
    seen = set()
    unique_lines = []
    for line in lines:
        line_clean = line.strip()
        # Only check for duplicates in non-formatted lines
        if line_clean and (line_clean.startswith(("•", "-", "*", "1.", "2.", "3.", "4.", "5.")) or 
                          line_clean not in seen):
            seen.add(line_clean)
            unique_lines.append(line)
    
    text = "\n".join(unique_lines).strip()
    
    # ✅ Stop at meta-commentary or self-dialogue (but preserve the answer)
    stop_phrases = [
        "ATHENA:",
        "Student:",
        "Now let me",
        "Let me continue",
    ]
    
    for stop in stop_phrases:
        # Only split if it appears on its own line or after significant content
        if f"\n{stop}" in text:
            text = text.split(f"\n{stop}")[0].strip()
        elif text.count(stop) > 1:  # Only if it appears more than once
            text = text.split(stop)[0].strip()
    
    return text



def should_use_simple_response(question: str) -> bool:
    """
    Check if the question is a simple greeting or conversational input
    that should get a contextual response instead of RAG retrieval
    
    Args:
        question: The user's question
        
    Returns:
        bool: True if this is a simple greeting/conversational query
    """
    import re
    
    question_lower = question.lower().strip()
    
    # Simple greetings that should get contextual response
    # Using word boundaries and looser matching for flexibility
    simple_patterns = [
        r"\b(hello|hi|hey|greetings|good\s*(morning|afternoon|evening|night)|what'?s\s*up|howdy)\b",
        r"^(how\s+are\s+you|how\s+do\s+you\s+do)",
        r"\b(what\s+is\s+your\s+name|who\s+are\s+you)\b",
        r"\b(can\s+you\s+help|help\s+me|i\s+need\s+help)\b",
        r"\b(thanks|thank\s+you|appreciate)\b",
    ]
    
    for pattern in simple_patterns:
        if re.search(pattern, question_lower):
            return True
    
    return False


def get_contextual_response(question: str) -> str:
    """
    Generate a context-aware response for simple conversational queries
    
    Args:
        question: The user's question
        
    Returns:
        str: A contextual response that acknowledges the user's input
    """
    question_lower = question.lower().strip()
    
    # Greeting responses
    if re.match(r"^(hello|hi|hey|greetings?|what'?s\s*up|howdy)", question_lower):
        return ("Hello! I'm ATHENA, your AI academic mentor. I'm here to help you learn and understand "
                "topics in Python, data structures, algorithms, machine learning, and deep learning. "
                "What would you like to learn about today?")
    
    if re.match(r"^(good\s*(morning|afternoon|evening|night))", question_lower):
        return ("Good day! I'm ATHENA, your academic mentor. I'm ready to help you with any academic questions "
                "you have. What topic would you like to explore?")
    
    if re.match(r"^(how\s*are\s*you|how\s*are\s*you\s*doing|how\s*do\s*you\s*do)", question_lower):
        return ("I'm operating perfectly! Ready to assist with your learning. I can help you understand Python, "
                "data structures, algorithms, ML, and DL concepts. What would you like to know?")
    
    if re.match(r"^(what\s*is\s*your\s*name|who\s*are\s*you)", question_lower):
        return ("I'm ATHENA, the AI Academic Mentor for ESPRIM students. I specialize in explaining complex "
                "concepts in Python, data structures, algorithms, machine learning, and deep learning in a "
                "clear, beginner-friendly way. What can I teach you?")
    
    if re.match(r"^(can\s*you\s*help|help\s*me|i\s*need\s*help)", question_lower):
        return ("Absolutely! I'm here to help. I can explain concepts, answer questions about Python, "
                "data structures, algorithms, machine learning, and deep learning. What topic would you like help with?")
    
    if re.match(r"^(thanks|thank\s*you|appreciate)", question_lower):
        return ("You're welcome! Happy to help. Feel free to ask me any other questions about your studies. "
                "What else can I explain for you?")
    
    # Default contextual response for other conversational inputs
    return ("I appreciate you reaching out! I'm ATHENA, here to help with your academic questions. "
            "Please ask me something specific about Python, algorithms, data structures, machine learning, or deep learning.")


async def generate_athena_answer(question: str) -> str:
    """
    Generate an answer using ATHENA RAG pipeline or contextual response
    
    This function checks if the question is a simple greeting first.
    For simple greetings/conversational input, it returns a contextual response.
    For academic questions, it uses the RAG chain (FAISS retriever + ATHENA prompt + LLM)
    to ensure ATHENA provides relevant educational answers.
    
    Args:
        question: The user's question
        
    Returns:
        str: ATHENA's generated answer with context and personality
    """
    # Declare globals at the start
    global vectorstore, llm, rag_chain, last_context
    
    try:
        # Check if this is a simple greeting or conversational input
        if should_use_simple_response(question):
            print(f"\n🤔 Question: {question}")
            print("💬 Using contextual response for greeting/conversational input")
            answer = get_contextual_response(question)
            last_context = "Conversational greeting/acknowledgment"
            print(f"✅ Contextual response generated")
            return answer
        
        # Ensure models are loaded
        
        if vectorstore is None:
            load_faiss_index()
        
        if llm is None:
            load_mistral_model()
        
        if rag_chain is None:
            build_rag_chain()
        
        print(f"\n🤔 Question: {question}")
        
        # ✅ Retrieve context and store it for API response
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        docs = await retriever.ainvoke(question)
        context = combine_docs(docs)
        last_context = context  # Store for get_last_context()
        
        print(f"📚 Context retrieved: {len(context)} chars")
        
        # ✅ ALWAYS USE RAG CHAIN - NO EXCEPTIONS
        # This ensures: FAISS retrieval → context assembly → ATHENA prompt → LLM generation
        print("🔄 Using RAG chain for answer generation...")
        result = await rag_chain.ainvoke(question)
        
        # Extract text from result
        if hasattr(result, 'text'):
            answer = result.text
        elif isinstance(result, str):
            answer = result
        else:
            answer = str(result)
        
        # Clean the output
        answer = clean_output(answer)
        
        print(f"✅ Answer generated successfully using RAG pipeline")
        
        return answer
        
    except Exception as e:
        print(f"❌ Error generating answer: {str(e)}")
        raise


def initialize_athena():
    """Initialize ATHENA models on startup"""
    try:
        print("\n" + "="*70)
        print("🚀 Initializing ATHENA AI Assistant")
        print("="*70)
        
        # Load all components
        load_faiss_index()
        load_mistral_model()
        build_rag_chain()
        
        print("\n" + "="*70)
        print("✅ ATHENA is ready to assist students!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Failed to initialize ATHENA: {str(e)}")
        raise


# Optional: Initialize on module import (comment out if you want lazy loading)
# initialize_athena()
