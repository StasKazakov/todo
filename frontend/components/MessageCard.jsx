"use client";
import React from "react";
import { Card } from "./ui/card";

export default function MessageCard({ msg }) {
  return (
    <Card
      className={`my-1 p-3 w-full min-h-5 bg-[#222125] text-white border-0`}
    >
      {msg.content}
      {msg.role === "assistant" && msg.sources && (
        <div className="mt-2 text-sm text-gray-400">
          Sources: {msg.sources.map((s) => `Page ${s.page}`).join(", ")}
        </div>
      )}
    </Card>
  );
}