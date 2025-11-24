from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

# Setup paths & env
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / "backend" / ".env")
CHROMA_DB_DIR = BASE_DIR / "backend" / "chroma_db"

# --- DEFINIÇÃO DO SCHEMA ---
class SearchInput(BaseModel):
    """Schema para garantir que o LLM chame a função corretamente."""
    query: str = Field(description="A string de busca específica. Ex: 'comida fria', 'atraso na entrega'")

class FoodReviewAgent:
    def __init__(self):
        self.setup_agent()

    def setup_agent(self):
        """Initializes the LLM, Vector Store, and LangGraph Agent."""
        
        # 1. LLM
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

        # 2. Vector Store
        embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        vector_store = Chroma(
            persist_directory=str(CHROMA_DB_DIR),
            embedding_function=embedding_function,
            collection_name="restaurant_reviews"
        )
        
        # 3. Tools Implementation
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        def search_func(query: str) -> str:
            # O Agente vai passar 'query' aqui
            docs = retriever.invoke(query)
            if not docs:
                return "Nenhum review encontrado sobre esse assunto."
            return "\n\n".join([f"Review: {d.page_content}" for d in docs])

        # Criação da Tool com Tipagem Estrita
        retriever_tool = Tool(
            name="search_reviews",
            description="Searches for actual customer reviews. Useful for checking customer sentiment on specific topics.",
            func=search_func,
            args_schema=SearchInput
        )
        
        self.tools = [retriever_tool]

        # 4. System Prompt
        self.system_message = """You are the 'FoodReview Insights Agent', an expert analyst for iFood restaurants.
        Your goal is to help restaurant owners understand their feedback.
        
        GUIDELINES:
        1. ALWAYS use the 'search_reviews' tool to find real data before answering. Do not hallucinate reviews.
        2. If you find reviews, summarize the key points (Positive vs Negative).
        3. Respond in Portuguese (PT-BR).
        """

        # 5. Create Agent
        self.agent_executor = create_react_agent(self.llm, self.tools)

    def chat(self, user_input: str):
        try:
            messages = [
                SystemMessage(content=self.system_message),
                ("human", user_input)
            ]
            
            result = self.agent_executor.invoke({"messages": messages})
            return result["messages"][-1].content
            
        except Exception as e:
            # Log de erro detalhado para debug
            print(f"DEBUG ERROR: {e}")
            return f"Erro no processamento: {str(e)}"

if __name__ == "__main__":
    print("🚀 Initializing Agent with Strict Typing...")
    try:
        agent = FoodReviewAgent()
        print("🤖 Agent Ready! Testing...")
        print("-" * 50)
        
        query = "O que os clientes estão falando sobre a entrega?"
        print(f"User: {query}")
        
        # Invocação
        result = agent.chat(query)
        
        print("-" * 50)
        print(f"\nFinal Answer:\n{result}")
    except Exception as e:
        print(f"🔥 Critical Startup Error: {e}")