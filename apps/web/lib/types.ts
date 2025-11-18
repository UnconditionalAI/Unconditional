/**
 * TypeScript types for Unconditional frontend
 */

export type MessageRole = "user" | "assistant" | "system";

export type ResponseType = "normal" | "crisis";

export interface Message {
  role: MessageRole;
  content: string;
  timestamp: string;
}

export interface ConversationResponse {
  type: ResponseType;
  content: string;
  timestamp: string;
}

export interface CrisisResource {
  name: string;
  phone: string;
  available: string;
  description?: string;
}

export interface CrisisResponse {
  type: "crisis";
  content: string;
  resources: CrisisResource[];
  timestamp: string;
  session_locked: boolean;
}

export type APIResponse = ConversationResponse | CrisisResponse;
