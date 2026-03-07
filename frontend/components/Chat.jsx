"use client";
import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { ScrollArea } from "./ui/scroll-area";
import { sendMessage } from "../lib/api";
import MessageCard from "./MessageCard";
import UploadButton from "./UploadButton";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", content: input }]);
    setLoading(true);

    try {
      const res = await sendMessage(input);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.answer, sources: res.sources },
      ]);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="flex flex-1 flex-col h-full w-full p-4 gap-2">
      <ScrollArea className="flex-1 min-h-[60vh] border rounded-md p-2 w-[75%] mx-auto max-h-[60vh]">
          {messages.map((msg, idx) => (
            <MessageCard key={idx} msg={msg} />
          ))}
          {loading && <p className="text-gray-500">Loading...</p>}
      </ScrollArea>

      <div className="flex gap-2 mt-2 w-[75%] mx-auto items-stretch">
        <Input
          className="flex-1 h-10"
          placeholder="Type your question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <UploadButton />
        <Button className="h-10" onClick={handleSend}>
          Send
        </Button>
      </div>
    </div>
  );
}