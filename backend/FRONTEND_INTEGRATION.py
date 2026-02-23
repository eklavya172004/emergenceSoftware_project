"""
Frontend Integration Guide
Connect React components to database API endpoints
"""

# Frontend Integration Code Examples

REACT_SETUP = `
// api/client.ts - Create API client
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = {
  // Conversation endpoints
  startConversation: async (userName: string, userEmail?: string) => {
    const response = await axios.post(\`\${API_URL}/conversations/start\`, {
      user_name: userName,
      user_email: userEmail
    });
    return response.data;
  },

  sendMessage: async (message: string, conversationId: string) => {
    const response = await axios.post(
      \`\${API_URL}/conversations/message-with-history\`,
      {
        message,
        conversation_id: conversationId
      }
    );
    return response.data;
  },

  getConversations: async (userName: string) => {
    const response = await axios.get(\`\${API_URL}/conversations/\${userName}\`);
    return response.data;
  },

  getConversationHistory: async (conversationId: string) => {
    const response = await axios.get(
      \`\${API_URL}/conversations/conversation/\${conversationId}\`
    );
    return response.data;
  },

  deleteConversation: async (conversationId: string) => {
    const response = await axios.delete(
      \`\${API_URL}/conversations/conversation/\${conversationId}\`
    );
    return response.data;
  },

  archiveConversation: async (conversationId: string) => {
    const response = await axios.post(
      \`\${API_URL}/conversations/conversation/\${conversationId}/archive\`
    );
    return response.data;
  },

  checkDBHealth: async () => {
    const response = await axios.get(\`\${API_URL}/conversations/db-health\`);
    return response.data;
  }
};
`

REACT_COMPONENT = `
// components/ChatWithDatabase.tsx
import React, { useState, useEffect, useRef } from 'react';
import { api } from '@/api/client';

interface Message {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  created_at?: string;
  tokens_used?: number;
}

interface Conversation {
  id: string;
  user_name: string;
  user_email?: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: string;
}

const ChatWithDatabase: React.FC = () => {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [userName, setUserName] = useState('Visitor');
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Start a new conversation
  const handleStartConversation = async () => {
    try {
      setLoading(true);
      const response = await api.startConversation(userName);
      setConversationId(response.conversation_id);
      setMessages([]);
      setLoading(false);
    } catch (error) {
      console.error('Error starting conversation:', error);
      setLoading(false);
    }
  };

  // Send message
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Start conversation if needed
    if (!conversationId) {
      await handleStartConversation();
      return;
    }

    try {
      setLoading(true);

      // Add user message to UI
      const userMessage: Message = { role: 'user', content: input };
      setMessages(prev => [...prev, userMessage]);

      // Send to API
      const response = await api.sendMessage(input, conversationId);

      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        tokens_used: response.tokens_used,
        created_at: response.created_at
      };
      setMessages(prev => [...prev, assistantMessage]);

      setInput('');
      setLoading(false);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, there was an error processing your request.'
        }
      ]);
      setLoading(false);
    }
  };

  // Load conversation history
  const handleLoadConversation = async (convId: string) => {
    try {
      setLoading(true);
      const response = await api.getConversationHistory(convId);
      setConversationId(convId);
      setMessages(response.messages || []);
      setShowHistory(false);
      setLoading(false);
    } catch (error) {
      console.error('Error loading conversation:', error);
      setLoading(false);
    }
  };

  // Load user's conversations
  const handleLoadConversations = async () => {
    try {
      const response = await api.getConversations(userName);
      setConversations(response.conversations || []);
      setShowHistory(true);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  // Delete conversation
  const handleDeleteConversation = async (convId: string) => {
    try {
      await api.deleteConversation(convId);
      setConversations(prev => prev.filter(c => c.id !== convId));
      if (conversationId === convId) {
        setConversationId(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-900 to-black">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <input
              type="text"
              value={userName}
              onChange={e => setUserName(e.target.value)}
              placeholder="Your name"
              className="bg-gray-700 text-white px-3 py-2 rounded w-40"
            />
            <button
              onClick={handleStartConversation}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-medium transition"
            >
              New Chat
            </button>
            <button
              onClick={handleLoadConversations}
              className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded transition"
            >
              History
            </button>
          </div>
          {conversationId && (
            <div className="text-gray-400 text-sm">
              Conv: {conversationId.slice(0, 8)}...
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden flex">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="h-full flex items-center justify-center text-gray-500">
                <div className="text-center">
                  <p className="text-lg font-medium mb-2">Start a conversation</p>
                  <p className="text-sm">Click "New Chat" or select from history</p>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={\`flex \${msg.role === 'user' ? 'justify-end' : 'justify-start'}\`}
              >
                <div
                  className={\`max-w-xs lg:max-w-md px-4 py-2 rounded-lg \${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-100'
                  }\`}
                >
                  <p>{msg.content}</p>
                  {msg.tokens_used && (
                    <p className="text-xs opacity-70 mt-1">
                      Tokens: {msg.tokens_used}
                    </p>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-lg">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-700 p-4 bg-gray-800">
            <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto flex gap-2">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Type your message..."
                disabled={!conversationId || loading}
                className="flex-1 bg-gray-700 text-white px-4 py-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!conversationId || loading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded font-medium transition disabled:opacity-50"
              >
                Send
              </button>
            </form>
          </div>
        </div>

        {/* History Sidebar */}
        {showHistory && (
          <div className="w-64 bg-gray-800 border-l border-gray-700 p-4 overflow-y-auto">
            <h3 className="text-white font-semibold mb-4">Conversations</h3>
            <div className="space-y-2">
              {conversations.map(conv => (
                <div
                  key={conv.id}
                  className="bg-gray-700 p-3 rounded cursor-pointer hover:bg-gray-600 transition group"
                >
                  <button
                    onClick={() => handleLoadConversation(conv.id)}
                    className="w-full text-left text-sm"
                  >
                    <p className="text-white font-medium truncate">{conv.title}</p>
                    <p className="text-gray-400 text-xs mt-1">
                      {new Date(conv.created_at).toLocaleDateString()}
                    </p>
                  </button>
                  <button
                    onClick={() => handleDeleteConversation(conv.id)}
                    className="text-red-400 hover:text-red-300 text-xs mt-2 opacity-0 group-hover:opacity-100 transition"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatWithDatabase;
`

ENV_SETUP = `
// .env.local
REACT_APP_API_URL=http://localhost:8000/api/v1

# For production:
# REACT_APP_API_URL=https://your-backend-domain.com/api/v1
`

PACKAGE_JSON = `
// Add to package.json dependencies
{
  "dependencies": {
    "axios": "^1.6.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^6.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.0.0"
  }
}
`

DEPLOYMENT_GUIDE = `
# Deployment Configuration

## Frontend Deployment (Vercel/Netlify)

1. Add environment variable in deployment platform:
   REACT_APP_API_URL=https://your-backend-domain.com/api/v1

2. Deploy:
   npm run build
   Deploy the build folder

## Backend Deployment (Railway/Render)

1. Set DATABASE_URL environment variable
2. Ensure CORS allows frontend domain:
   CORS_ORIGINS=https://your-frontend-domain.com

## CORS Configuration

Update backend/app/main.py:

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
`

if __name__ == "__main__":
    print("=== Frontend Integration Guide ===\n")
    print("1. API Client Setup:")
    print(REACT_SETUP)
    print("\n2. React Component:")
    print(REACT_COMPONENT)
    print("\n3. Environment Variables:")
    print(ENV_SETUP)
    print("\n4. Package Dependencies:")
    print(PACKAGE_JSON)
    print("\n5. Deployment Configuration:")
    print(DEPLOYMENT_GUIDE)
