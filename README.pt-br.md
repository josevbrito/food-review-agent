# 🍔 FoodReview Insights Agent

<div align="center">

[![English](https://img.shields.io/badge/Read_in-English-blue?style=for-the-badge)](./README.md)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange?style=for-the-badge)

**Um Agente Autônomo de IA capaz de extrair insights estratégicos de reviews desestruturados.**

</div>

---

## 🚀 Sobre o Projeto

Desenvolvido com foco em **Engenharia de GenAI**, este projeto simula um analista inteligente para donos de restaurantes parceiros (cenário iFood).

Diferente de sistemas RAG simples, este agente utiliza um **Motor de Raciocínio (ReAct)** via **LangGraph** para entender perguntas complexas, gírias brasileiras e feedbacks "sujos" (com erros de português e caps lock), transformando dados brutos em inteligência de negócio.

### 🏗️ Arquitetura Técnica

* **Cérebro:** Llama 3.3 70B (Groq)
* **Orquestração:** LangGraph (Framework moderno de Agentes)
* **Memória (RAG):** ChromaDB (Local) + HuggingFace Embeddings
* **Backend:** FastAPI (Python)
* **Frontend:** Next.js 15 (Interface Terminal Cyberpunk)
* **Engenharia de Dados:** Pipeline de Geração Sintética para simular reviews reais e caóticos.

---

## 🛠️ Como Rodar Localmente

### 1. Clone e Instale
```bash
git clone https://github.com/josevbrito/food-review-agent.git
cd food-review-agent

# Criação do ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalação das dependências
pip install -r backend/requirements.txt
````

### 2\. Configuração de Variáveis

Crie um arquivo `backend/.env` baseado no `backend/.env.example`:

```ini
GROQ_API_KEY=gsk_sua_chave_aqui
```

### 3\. Geração de Dados e Iniciação do Backend

Este script usa o Llama 3 para gerar reviews sintéticos (simulando clientes reais/bravos) e popula o banco vetorial.

```bash
# A partir da raiz do projeto
cd backend
python app/scripts/generate_synthetic_data.py
uvicorn app.main:app --reload
```

### 4\. Iniciar Frontend

Abra um novo terminal:

```bash
cd frontend
npm install
npm run dev
```

Acesse a interface em `http://localhost:3000`.

-----

## 🧪 Testando o Agente

Tente fazer perguntas que exijam raciocínio e leitura de contexto:

  * *"O que falam sobre a entrega?"* (Análise de Sentimento)
  * *"Tem reclamações sobre o Sushi?"* (Busca Específica)
  * *"O pessoal está bravo?"* (Interpretação de "Caps Lock" e tom de voz)

-----

## 👨‍💻 Autor

**José Victor Brito Costa**
* Engenheiro de Software & Cientista de Dados
* Foco: LLMOps, Agentes e Desenvolvimento Full Stack.

<div align="left"> 
  <a href="https://josevbrito.com" target="_blank">
    <img src="https://img.shields.io/badge/Portfólio-Visitar_Site-00ff41?style=for-the-badge&logo=vercel&logoColor=black" alt="Portfolio">
  </a>
  <a href="https://www.linkedin.com/in/josevbrito" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-Conectar-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn">
  </a>
</div>

<br />

> **Se este projeto te ajudou ou você curtiu a arquitetura, deixe uma ⭐️ no topo da página!**