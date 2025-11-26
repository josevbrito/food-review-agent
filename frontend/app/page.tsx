"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Sparkles, ChefHat, TrendingUp, MessageSquare } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function FoodReviewAgent() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: "assistant", 
      content: "Olá! 👋 Sou seu assistente de análise de reviews de delivery.\n\nPosso te ajudar a extrair insights sobre restaurantes, qualidade dos pedidos, tempo de entrega e muito mais. Como posso ajudar?" 
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!res.ok) throw new Error("Falha na API");

      const data = await res.json();
      
      setMessages((prev) => [
        ...prev, 
        { role: "assistant", content: data.response }
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev, 
        { role: "assistant", content: "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const quickPrompts = [
    { icon: TrendingUp, text: "Principais insights do dataset", color: "from-emerald-500 to-teal-500" },
    { icon: ChefHat, text: "Restaurantes mais bem avaliados", color: "from-violet-500 to-purple-500" },
    { icon: MessageSquare, text: "Análise de sentimentos", color: "from-blue-500 to-cyan-500" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 flex flex-col h-screen max-w-5xl mx-auto p-4 md:p-6">
        {/* Header */}
        <header className="mb-6 pt-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                  FoodReview AI
                </h1>
                <p className="text-sm text-slate-400">Análise Inteligente de Reviews</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs text-emerald-400">
              <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
              <span className="hidden sm:inline">Online</span>
            </div>
          </div>
        </header>

        {/* Chat Container */}
        <div className="flex-1 bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800/50 shadow-2xl flex flex-col overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
            {messages.length === 1 && (
              <div className="mb-6">
                <p className="text-slate-400 text-sm mb-4">Experimente perguntar:</p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {quickPrompts.map((prompt, idx) => (
                    <button
                      key={idx}
                      onClick={() => setInput(prompt.text)}
                      className="group p-4 bg-slate-800/50 hover:bg-slate-800 rounded-xl border border-slate-700/50 hover:border-slate-600 transition-all text-left"
                    >
                      <div className={`w-8 h-8 mb-2 bg-gradient-to-br ${prompt.color} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}>
                        <prompt.icon className="w-4 h-4 text-white" />
                      </div>
                      <p className="text-sm text-slate-300">{prompt.text}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}
              >
                <div className={`max-w-[85%] md:max-w-[75%] ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-emerald-500 to-teal-500 text-white rounded-2xl rounded-tr-sm'
                    : 'bg-slate-800/50 border border-slate-700/50 text-slate-100 rounded-2xl rounded-tl-sm'
                } p-4 shadow-lg`}>
                  <div className="whitespace-pre-wrap leading-relaxed text-sm md:text-base">
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl rounded-tl-sm p-4 shadow-lg">
                  <div className="flex items-center gap-2 text-slate-400">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                    <span className="text-sm">Analisando...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-slate-800/50 bg-slate-900/50">
            <div className="flex gap-3 items-center">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Digite sua pergunta..."
                className="flex-1 bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 outline-none focus:border-emerald-500/50 focus:ring-2 focus:ring-emerald-500/20 transition-all"
                autoFocus
              />
              <button 
                onClick={handleSubmit}
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-br from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed p-3 rounded-xl transition-all shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/40 disabled:shadow-none group"
              >
                <Send className="w-5 h-5 text-white group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-4 text-center text-xs text-slate-500">
          <p>Powered by Llama 3 • LangGraph • RAG Technology</p>
        </footer>
      </div>
    </div>
  );
}