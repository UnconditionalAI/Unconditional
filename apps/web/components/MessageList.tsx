/**
 * Message list component
 * Displays conversation history with calm, minimal styling
 */

"use client";

import { Message } from "@/lib/types";

interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto px-4 py-8 space-y-6">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${
            message.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div
            className={`max-w-2xl px-6 py-4 rounded-lg ${
              message.role === "user"
                ? "bg-gray-100 text-gray-900"
                : "bg-gray-50 text-gray-800 border border-gray-200"
            }`}
          >
            <p className="whitespace-pre-wrap leading-relaxed">
              {message.content}
            </p>
            <time className="text-xs text-gray-500 mt-2 block">
              {new Date(message.timestamp).toLocaleTimeString()}
            </time>
          </div>
        </div>
      ))}
    </div>
  );
}
