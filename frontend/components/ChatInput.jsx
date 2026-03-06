'use client';

import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="flex gap-2 mt-4">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your question..."
        className="flex-1 p-2 border rounded-md"
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button
        onClick={handleSend}
        className="px-4 py-2 bg-blue-500 text-white rounded-md"
      >
        Send
      </button>
    </div>
  );
}