/**
 * LocalStorage-based conversation persistence
 *
 * Safety reasoning:
 * - All data stays client-side
 * - User controls their own data
 * - No server-side storage = no breach risk
 * - Easy export/delete for user
 */

import { Message } from "./types";

const STORAGE_KEY = "unconditional_conversation";

export interface ConversationState {
  messages: Message[];
  sessionLocked: boolean;
  lastUpdated: string;
}

/**
 * Load conversation from localStorage
 */
export function loadConversation(): ConversationState | null {
  if (typeof window === "undefined") return null;

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;

    return JSON.parse(stored);
  } catch (error) {
    console.error("[STORAGE] Failed to load conversation:", error);
    return null;
  }
}

/**
 * Save conversation to localStorage
 */
export function saveConversation(state: ConversationState): void {
  if (typeof window === "undefined") return;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    console.error("[STORAGE] Failed to save conversation:", error);
  }
}

/**
 * Clear conversation from localStorage
 */
export function clearConversation(): void {
  if (typeof window === "undefined") return;

  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error("[STORAGE] Failed to clear conversation:", error);
  }
}

/**
 * Export conversation as JSON
 */
export function exportConversation(): string | null {
  const state = loadConversation();
  if (!state) return null;

  return JSON.stringify(state, null, 2);
}
