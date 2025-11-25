import sys
import random
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Setup
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / "backend" / ".env")
CHROMA_DB_DIR = BASE_DIR / "backend" / "chroma_db"

def generate_and_ingest():
    print("Iniciando Geração de Dados...")
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=1.0)
    
    categories = ["Sushi", "Pizza", "Hambúrguer", "Açaí", "Marmita", "Cachorro-quente", "Doce e Bolo", "Salgado"]
    sentiments = ["Muito Positivo", "Positivo", "Neutro", "Negativo", "Muito Negativo"]
    
    # Personas para variar a escrita
    personas = [
        "Jovem de Internet (use abreviações como 'mt', 'vc', 'pq', 'n', sem pontuação, tudo minúsculo)",
        "Cliente Furioso (USE CAPS LOCK, MUITA EXCLAMAÇÃO!!!, indignado)",
        "Cliente com Pressa (cometa erros de digitação propositais, frases curtas, sem nexo)",
        "Cliente Detalhista (texto mais longo, focado na embalagem e temperatura)"
    ]
    
    reviews = []
    
    # Vamos gerar ~60 reviews
    print("⏳ Cozinhando... (Isso vai levar uns 40 segundos)")
    
    for category in categories:
        for sentiment in sentiments:
            # Escolhendo uma persona aleatória para cada review
            persona = random.choice(personas)
            
            try:
                prompt = f"""
                Atue como um cliente brasileiro real do iFood fazendo uma avaliação.
                Produto: {category}.
                Sentimento: {sentiment}.
                Persona: {persona}.
                
                IMPORTANTE: 
                - Não seja polido. Seja visceral.
                - Se for negativo, reclame do motoboy, do atraso ou da comida fria.
                - Se for positivo, elogie o sabor ou a entrega rápida.
                - Mantenha curto (máximo 2 frases).
                - Responda APENAS o texto do review, nada mais.
                """
                
                response = llm.invoke(prompt)
                review_text = response.content.strip().replace('"', '')
                
                # Lógica simples de Rating
                if "Muito Positivo" in sentiment: rating = 5
                elif "Positivo" in sentiment: rating = 4
                elif "Neutro" in sentiment: rating = 3
                elif "Negativo" in sentiment: rating = 2
                else: rating = 1
                
                reviews.append({
                    "text": review_text,
                    "rating": rating,
                    "category": category
                })
                
                print(f"[{rating}⭐] {review_text[:60]}...")
                
            except Exception as e:
                print(f"Erro: {e}")

    # --- Limpeza do Banco Antigo ---
    print("\n🧹 Limpando memória antiga...")
    import shutil
    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)

    # --- Ingestão ---
    print(f"🧠 Ingerindo {len(reviews)} reviews no ChromaDB...")
    
    documents = []
    for r in reviews:
        context = f"Rating: {r['rating']}/5. Category: {r['category']}. Review: {r['text']}"
        doc = Document(
            page_content=context,
            metadata={
                "rating": r["rating"],
                "category": r["category"],
                "source": "synthetic_chaos_v2"
            }
        )
        documents.append(doc)

    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embedding_function,
        collection_name="restaurant_reviews"
    )

    vector_store.add_documents(documents)
    print("🔥 Sucesso!")

if __name__ == "__main__":
    generate_and_ingest()