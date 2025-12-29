# app/services/rag_loader.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class AthenaRagPipeline:
    def __init__(self):
        print("🔄 Loading ATHENA RAG Pipeline...")

        # =============================
        # 1️⃣ Load Embeddings for FAISS
        # =============================
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # =============================
        # 2️⃣ Load FAISS Index
        # =============================
        self.vectorstore = FAISS.load_local(
            "athena_faiss_index",
            embeddings=self.embedding,
            allow_dangerous_deserialization=True,
        )
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3},
        )

        # =============================
        # 3️⃣ Load Mistral Model
        # =============================
        model_id = "mistralai/Mistral-7B-Instruct-v0.2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
        )

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=250,  # shorter, cleaner answers
            temperature=0.3,      # more stable & educational
            top_p=0.9,
            repetition_penalty=1.1,
        )

        print("✅ ATHENA RAG Pipeline Ready!")

    # =============================
    # Retrieve contextual FAISS knowledge
    # =============================
    def get_context(self, question: str):
        docs = self.retriever.invoke(question)
        if not docs:
            return None
        return "\n\n".join(d.page_content for d in docs)

    # =============================
    # Main reasoning + generation
    # =============================
    def answer(self, question: str, is_new_chat: bool = False):
        context = self.get_context(question)

        # =============================
        # ATHENA Persona
        # =============================
        system_prompt = """
Tu es ATHENA — l’assistante d’apprentissage intelligente de l’ESPRIM.
Tu es professionnelle, pédagogique, concise et bienveillante.
Tu ne donnes *jamais* de réponses vagues ou génériques.
Tu n’inventes rien hors contexte. Tu expliques clairement.
Tu ne poses pas de questions inutiles.
Tu ne génères pas de dialogues artificiels.
Tu ne fais pas de blabla ou de longues introductions.
"""

        # =============================
        # Welcoming message ONLY if:
        # - new conversation
        # - AND question is a greeting
        # =============================
        welcoming = ""
        if is_new_chat or question.lower().strip() in ["hello", "hi", "salut", "hey"]:
            welcoming = "Bonjour ! Comment puis-je t’aider dans ton apprentissage aujourd’hui ?\n\n"

        # =============================
        # If no FAISS context found
        # =============================
        if not context:
            context = (
                "Aucun contenu FAISS pertinent n’a été trouvé. "
                "Donne une explication courte, claire et académique adaptée à un étudiant."
            )

        # =============================
        # RAG Prompt Format
        # =============================
        prompt = f"""
{system_prompt}

📚 Contexte extrait :
{context}

❓ Question de l’étudiant :
{question}

✏️ Réponse d’ATHENA (claire, concise, structurée) :
"""

        # =============================
        # Generate answer
        # =============================
        generated = self.generator(prompt)[0]["generated_text"]

        # Extract clean answer (remove prompt)
        if "Réponse d’ATHENA" in generated:
            answer = generated.split("Réponse d’ATHENA")[-1]
        else:
            answer = generated

        answer = answer.replace(prompt, "").strip()

        # Final cleanup
        answer = answer.replace("🧠", "").replace("🔴", "")
        answer = answer.replace("Réponse :", "").strip()

        # Add welcoming line if needed
        if welcoming:
            answer = welcoming + answer

        return {
            "answer": answer,
            "context_used": context,
        }


# Singleton instance so the model loads only once
athena_rag = AthenaRagPipeline()
