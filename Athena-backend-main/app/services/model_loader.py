"""
ATHENA Model Loader - GPU-optimized with automatic CPU fallback
Optimized for GTX 1650 (4GB VRAM) using 4-bit quantization
"""
import os
import torch
from typing import Callable, List, Tuple
from pathlib import Path

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
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Global cache
_embeddings = None
_vectorstore = None
_llm = None
_rag_chain = None


def check_gpu_status():
    """Check and log GPU availability"""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🔥 GPU MODE ENABLED")
        print(f"   GPU: {gpu_name}")
        print(f"   VRAM: {vram_total:.2f} GB")
        return True
    else:
        print("⚠️ GPU not available → CPU fallback")
        return False


def load_embeddings():
    """Load sentence-transformers embedding model"""
    global _embeddings
    
    if _embeddings is not None:
        return _embeddings
    
    print("📥 Loading embedding model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    _embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': device}
    )
    
    print(f"✅ Embeddings loaded on {device.upper()}")
    return _embeddings


def load_faiss():
    """Load FAISS vector store"""
    global _vectorstore
    
    if _vectorstore is not None:
        return _vectorstore
    
    print("📥 Loading FAISS index...")
    
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found at {FAISS_INDEX_PATH}\n"
            "Run 'python create_faiss_index.py' first!"
        )
    
    embeddings = load_embeddings()
    _vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    print("✅ FAISS index loaded")
    return _vectorstore


def load_llm():
    """Load Mistral-7B with 4-bit quantization and GPU/CPU fallback"""
    global _llm
    
    if _llm is not None:
        return _llm
    
    # Check GPU status
    gpu_available = check_gpu_status()
    
    print("📥 Loading Mistral-7B-Instruct...")
    
    # Try GPU first with 4-bit quantization
    if gpu_available:
        try:
            print("   Attempting GPU load with 4-bit quantization...")
            
            # 4-bit quantization config
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16
            )
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            tokenizer.pad_token = tokenizer.eos_token
            
            # Load model with 4-bit quantization
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True
            )
            
            # Create pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=350,
                temperature=0.4,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True
            )
            
            _llm = HuggingFacePipeline(pipeline=pipe)
            
            print("✅ Mistral-7B loaded on GPU (4-bit)")
            print(f"   VRAM used: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
            return _llm
            
        except Exception as e:
            print(f"⚠️ GPU load failed: {e}")
            print("   Falling back to CPU...")
    
    # CPU fallback - no quantization
    try:
        print("   Loading on CPU without quantization (this will be slow and memory-intensive)...")
        
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        tokenizer.pad_token = tokenizer.eos_token
        
        # Load model on CPU without quantization
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map={"": "cpu"},
            torch_dtype=torch.float32,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=350,
            temperature=0.4,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True
        )
        
        _llm = HuggingFacePipeline(pipeline=pipe)
        
        print("✅ Mistral-7B loaded on CPU")
        print("⚠️  WARNING: CPU inference will be extremely slow (30-120 seconds per answer)")
        return _llm
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        raise


def format_docs(docs: List[Document]) -> str:
    """Format retrieved documents into context string"""
    return "\n\n".join(doc.page_content for doc in docs)


def rag_chain() -> Tuple[Callable, Callable]:
    """
    Build and return RAG chain with retriever
    Returns: (chain_function, retriever_function)
    """
    global _rag_chain
    
    if _rag_chain is not None:
        return _rag_chain
    
    print("🔗 Building RAG chain...")
    
    # Load components
    vectorstore = load_faiss()
    llm = load_llm()
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # Define prompt template
    template = """You are ATHENA, an educational AI assistant.
Your tone is clear, positive, structured, and pedagogical.

Use this structure:
🌟 Introduction
📘 Explanation
💡 Example
🎓 Summary

Context:
{context}

Question:
{question}

Answer:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # Build RAG chain
    def run_chain(question: str) -> str:
        """Execute RAG chain"""
        # Retrieve documents
        docs = retriever.invoke(question)
        context = format_docs(docs)
        
        # Generate answer
        chain = prompt | llm
        result = chain.invoke({"context": context, "question": question})
        
        # Clean output
        if isinstance(result, str):
            answer = result
        else:
            answer = result.get("text", str(result))
        
        # Remove common artifacts
        answer = answer.strip()
        if answer.startswith("Answer:"):
            answer = answer[7:].strip()
        
        return answer
    
    # Store chain and retriever
    _rag_chain = (run_chain, retriever)
    
    print("✅ RAG chain ready")
    return _rag_chain


def get_answer_with_sources(question: str) -> Tuple[str, List[str]]:
    """
    Generate answer with source chunks
    Returns: (answer, source_chunks)
    """
    chain_fn, retriever = rag_chain()
    
    # Get source documents
    docs = retriever.invoke(question)
    sources = [doc.page_content for doc in docs]
    
    # Generate answer
    answer = chain_fn(question)
    
    return answer, sources
