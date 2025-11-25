"use client";

import { useState, useRef, useEffect } from "react";
import { Terminal, Loader2, Send } from "lucide-react";
import { motion } from "framer-motion";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "SYSTEM ONLINE.\nFoodReview Insights Agent v1.0 conectado.\nDataset: SYNTHETIC_DELIVERY_V2.\n\nComo posso ajudar hoje?" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      // Chama o Backend via Proxy
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
        { role: "assistant", content: "ERRO CRÍTICO: Falha na conexão com o servidor neural." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-12 relative bg-black selection:bg-[#00ff41] selection:text-black">
      <div className="scanline inset-0 absolute pointer-events-none fixed h-screen w-screen" />

      <div className="z-10 w-full max-w-5xl bg-black/90 border border-[#00ff41] shadow-[0_0_30px_rgba(0,255,65,0.15)] rounded-sm overflow-hidden flex flex-col h-[85vh]">
        
        {/* Header */}
        <div className="bg-[#00ff41]/10 border-b border-[#00ff41] p-3 flex items-center justify-between backdrop-blur-sm">
          <div className="flex items-center gap-3 text-[#00ff41]">
            <Terminal size={18} />
            <h1 className="font-bold tracking-widest text-sm md:text-base">FOOD_REVIEW_AGENT // ROOT_ACCESS</h1>
          </div>
          <div className="flex items-center gap-2 text-[10px] md:text-xs text-[#00ff41]/80 font-mono">
            <span className="hidden md:inline">MEMORY: 64TB</span>
            <span>|</span>
            <div className="w-2 h-2 bg-[#00ff41] rounded-full animate-pulse" />
            <span>ONLINE</span>
          </div>
        </div>

        {/* Chat */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 font-mono scrollbar-thin">
          {messages.map((msg, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[85%] md:max-w-[75%] p-3 md:p-4 rounded-sm border ${
                msg.role === 'user' 
                  ? 'border-[#00ff41]/50 bg-[#00ff41]/10 text-[#00ff41] ml-auto' 
                  : 'border-transparent bg-transparent text-[#00ff41] pl-0'
              }`}>
                <div className="flex items-center gap-2 mb-1 text-[10px] opacity-60 uppercase tracking-wider font-bold">
                  {msg.role === 'user' ? '> USER_INPUT' : '> AI_OUTPUT'}
                </div>
                <div className="whitespace-pre-wrap leading-relaxed text-sm md:text-base shadow-black drop-shadow-md">
                  {msg.content}
                </div>
              </div>
            </motion.div>
          ))}
          
          {isLoading && (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }}
              className="flex justify-start pl-0"
            >
              <div className="flex items-center gap-3 text-[#00ff41]/70 p-4 font-mono text-sm">
                <Loader2 className="animate-spin" size={16} />
                <span className="animate-pulse tracking-widest">PROCESSANDO DADOS...</span>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 bg-black border-t border-[#00ff41]/30">
          <form onSubmit={handleSubmit} className="flex gap-3 items-center">
            <span className="text-[#00ff41] font-bold text-xl">{'>'}</span>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite seu comando..."
              className="flex-1 bg-transparent border-none outline-none text-[#00ff41] font-mono placeholder-[#00ff41]/30 text-base md:text-lg"
              autoFocus
            />
            <button 
              type="submit" 
              disabled={isLoading || !input.trim()}
              className="p-2 hover:bg-[#00ff41]/20 rounded-full transition-colors disabled:opacity-30 text-[#00ff41]"
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}