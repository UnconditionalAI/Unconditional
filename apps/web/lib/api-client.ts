/**
 * API client for Unconditional backend
 */

import { APIResponse, Message } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * Get opening message from API
 */
export async function getOpeningMessage(): Promise<APIResponse> {
  const response = await fetch(`${API_BASE_URL}/opening`);

  if (!response.ok) {
    throw new Error(`Failed to get opening message: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Send message and get response
 */
export async function sendMessage(
  content: string,
  history: Message[]
): Promise<APIResponse> {
  const response = await fetch(`${API_BASE_URL}/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content,
      history: {
        messages: history.map((m) => ({
          role: m.role,
          content: m.content,
        })),
      },
    }),
  });

  if (!response.ok) {
    // Handle banned content or other errors
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(error.detail || "Invalid message");
    }

    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}
