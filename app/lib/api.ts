/**
 * API Client for Portfolio Backend
 * Handles all communication with the FastAPI backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Types
export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  conversation_history?: Message[];
}

export interface ChatResponse {
  message: string;
  role: 'assistant';
  timestamp?: string;
  conversation_id?: string;
}

export interface ConversationStartRequest {
  user_name?: string;
  user_email?: string;
}

export interface ConversationResponse {
  conversation_id: string;
  user_name: string;
  created_at?: string;
}

export interface ConversationHistoryResponse {
  conversation_id: string;
  messages: Message[];
}

export interface ConversationListResponse {
  total: number;
  conversations: Array<{
    conversation_id: string;
    user_name: string;
    created_at: string;
  }>;
}

/**
 * API Client class with all methods for backend communication
 */
export class PortfolioAPI {
  private apiUrl: string;

  constructor(baseUrl: string = API_URL) {
    this.apiUrl = baseUrl;
  }

  /**
   * Send a message and get AI response
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/conversations/message-with-history`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Start a new conversation
   */
  async startConversation(request: ConversationStartRequest): Promise<ConversationResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/conversations/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error('Failed to start conversation');
      }

      return await response.json();
    } catch (error) {
      console.error('Error starting conversation:', error);
      throw error;
    }
  }

  /**
   * Get conversation history by ID
   */
  async getConversationHistory(
    conversationId: string,
  ): Promise<ConversationHistoryResponse> {
    try {
      const response = await fetch(
        `${this.apiUrl}/conversations/conversation/${conversationId}`,
      );

      if (!response.ok) {
        throw new Error('Failed to fetch conversation history');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching conversation history:', error);
      throw error;
    }
  }

  /**
   * Get all conversations for a user
   */
  async getUserConversations(userName: string): Promise<ConversationListResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/conversations/${userName}`);

      if (!response.ok) {
        throw new Error('Failed to fetch conversations');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching user conversations:', error);
      throw error;
    }
  }

  /**
   * Delete a conversation
   */
  async deleteConversation(conversationId: string): Promise<void> {
    try {
      const response = await fetch(
        `${this.apiUrl}/conversations/conversation/${conversationId}`,
        {
          method: 'DELETE',
        },
      );

      if (!response.ok) {
        throw new Error('Failed to delete conversation');
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      throw error;
    }
  }

  /**
   * Check database health
   */
  async checkHealth(): Promise<{ status: string }> {
    try {
      const response = await fetch(`${this.apiUrl}/conversations/db-health`);

      if (!response.ok) {
        throw new Error('Health check failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }
}

// Create singleton instance
export const api = new PortfolioAPI();

/**
 * Helper function to format timestamp
 */
export function formatTime(timestamp?: string): string {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
}

/**
 * Helper function to format date
 */
export function formatDate(timestamp?: string): string {
  if (!timestamp) return 'Today';
  const date = new Date(timestamp);
  const today = new Date();
  
  if (date.toDateString() === today.toDateString()) {
    return 'Today';
  }
  
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  
  if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday';
  }
  
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined,
  });
}
