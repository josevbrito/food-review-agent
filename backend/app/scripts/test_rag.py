import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(BASE_DIR))

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Carrega variáveis de ambiente
load_dotenv(BASE_DIR / "backend" / ".env")

CHROMA_DB_DIR = BASE_DIR / "backend" / "chroma_db"

def test_retrieval():
    print("🧠 Carregando Vector Store (Memória)...")
    
    # 1. Inicializa o mesmo modelo de embeddings usado na ingestão
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 2. Conecta ao ChromaDB existente no disco
    vector_store = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embedding_function,
        collection_name="restaurant_reviews"
    )

    print("✅ Vector Store carregado com sucesso!")
    print("-" * 50)
    print("🔎 Ferramenta de Teste RAG (Digite 'sair' para encerrar)")
    
    while True:
        query = input("\n📝 O que você quer buscar nas reviews? ")
        if query.lower() in ['exit', 'quit', 'sair']:
            break
            
        print(f"🔍 Buscando por conceitos similares a: '{query}'...")
        
        # 3. Executa a Busca por Similaridade (Similarity Search)
        # k=3 -> top 3 resultados mais próximos
        results = vector_store.similarity_search(query, k=3)
        
        if not results:
            print("❌ Nenhum resultado encontrado.")
            continue

        print(f"\nEncontrei {len(results)} reviews relevantes:\n")
        
        for i, doc in enumerate(results):
            rating = doc.metadata.get('rating', 'N/A')
            date = doc.metadata.get('date', 'N/A')
            content = doc.page_content
            
            # Mostra os primeiros 300 caracteres
            print(f"--- Resultado {i+1} (⭐ {rating}/5 | 📅 {date}) ---")
            print(f"📄 \"{content[:300]}...\"")
            print()

if __name__ == "__main__":
    test_retrieval()