/**
 * Main conversation view component
 * Orchestrates message list, input, and API interactions
 */

"use client";

import { useEffect, useState } from "react";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import { CrisisScreen } from "./CrisisScreen";
import { getOpeningMessage, sendMessage } from "@/lib/api-client";
import { Message, CrisisResource } from "@/lib/types";
import {
  loadConversation,
  saveConversation,
  clearConversation,
} from "@/lib/storage";

export function ConversationView() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionLocked, setSessionLocked] = useState(false);
  const [crisisMessage, setCrisisMessage] = useState<string | null>(null);
  const [crisisResources, setCrisisResources] = useState<CrisisResource[]>([]);

  // Load conversation from localStorage on mount
  useEffect(() => {
    const stored = loadConversation();
    if (stored) {
      setMessages(stored.messages);
      setSessionLocked(stored.sessionLocked);
    } else {
      // Get opening message if no stored conversation
      getOpeningMessage().then((response) => {
        const openingMessage: Message = {
          role: "assistant",
          content: response.content,
          timestamp: response.timestamp,
        };
        setMessages([openingMessage]);
      });
    }
  }, []);

  // Save conversation to localStorage whenever it changes
  useEffect(() => {
    if (messages.length > 0) {
      saveConversation({
        messages,
        sessionLocked,
        lastUpdated: new Date().toISOString(),
      });
    }
  }, [messages, sessionLocked]);

  const handleSendMessage = async (content: string) => {
    if (sessionLocked) return;

    // Add user message immediately
    const userMessage: Message = {
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send to API with full history
      const response = await sendMessage(content, [...messages, userMessage]);

      if (response.type === "crisis") {
        // Handle crisis response
        const crisisResp = response as any; // Type assertion for crisis fields
        setCrisisMessage(crisisResp.content);
        setCrisisResources(crisisResp.resources);
        setSessionLocked(true);
      } else {
        // Handle normal response
        const assistantMessage: Message = {
          role: "assistant",
          content: response.content,
          timestamp: response.timestamp,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error("[API ERROR]", error);
      // Show error to user
      const errorMessage: Message = {
        role: "assistant",
        content:
          "I'm having trouble connecting right now. Please try again in a moment.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearConversation = () => {
    if (
      confirm(
        "Are you sure you want to clear this conversation? This cannot be undone."
      )
    ) {
      clearConversation();
      setMessages([]);
      setSessionLocked(false);
      setCrisisMessage(null);
      setCrisisResources([]);

      // Get new opening message
      getOpeningMessage().then((response) => {
        const openingMessage: Message = {
          role: "assistant",
          content: response.content,
          timestamp: response.timestamp,
        };
        setMessages([openingMessage]);
      });
    }
  };

  // Show crisis screen if session is locked
  if (sessionLocked && crisisMessage) {
    return (
      <div className="h-screen flex flex-col bg-white">
        <CrisisScreen message={crisisMessage} resources={crisisResources} />
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 p-4">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-900">
            Unconditional
          </h1>
          <button
            onClick={handleClearConversation}
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            Clear conversation
          </button>
        </div>
      </header>

      {/* Messages */}
      <MessageList messages={messages} />

      {/* Loading indicator */}
      {isLoading && (
        <div className="px-4 py-2 text-center text-sm text-gray-500">
          Thinking...
        </div>
      )}

      {/* Input */}
      <MessageInput onSend={handleSendMessage} disabled={sessionLocked} />
    </div>
  );
}
