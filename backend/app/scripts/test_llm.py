import sys
from pathlib import Path
from dotenv import load_dotenv

# Path setup
BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(BASE_DIR))

# Load Env
load_dotenv(BASE_DIR / "backend" / ".env")

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def test_llm_connection():
    print("🔌 Connecting to Groq API (Llama 3.3)...")
    
    try:
        # 1. Initialize LLM
        # temperature=0 ensures deterministic (factual) answers
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        # 2. Create a simple prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a specialized AI assistant for analyzing restaurant reviews."),
            ("human", "{question}")
        ])

        # 3. Create Chain
        chain = prompt | llm

        # 4. Invoke
        print("🧠 Sending test query...")
        response = chain.invoke({"question": "Explain in one sentence why analyzing customer feedback is crucial for a restaurant."})
        
        print("\n✅ Connection Successful!")
        print(f"🤖 AI Response: {response.content}")

    except Exception as e:
        print(f"\n❌ Connection Failed: {e}")
        print("Tip: Check your GROQ_API_KEY in backend/.env")

if __name__ == "__main__":
    test_llm_connection()