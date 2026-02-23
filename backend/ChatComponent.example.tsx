import React, { useState, FC, FormEvent, ChangeEvent } from 'react';

// API base URL - change this to your backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

const ChatComponent: FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Send message to backend API
   */
  const sendMessage = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          conversation_history: messages,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.message,
        timestamp: data.timestamp,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Error sending message:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
          </div>
        ))}
        {loading && <div className="message assistant loading">Thinking...</div>}
        {error && <div className="message error">{error}</div>}
      </div>

      <form onSubmit={sendMessage} className="chat-form">
        <input
          type="text"
          value={input}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
          placeholder="Ask me anything about my experience..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatComponent;

// ============================================
// SETUP INSTRUCTIONS FOR REACT FRONTEND
// ============================================

/*
1. INSTALL DEPENDENCIES
   No extra packages needed! React has fetch built-in.

2. CREATE .env FILE IN PROJECT ROOT
   REACT_APP_API_URL=http://localhost:8000

3. USE THE COMPONENT
   Import and add ChatComponent to your page:
   
   import ChatComponent from './ChatComponent';
   
   // In your page:
   <ChatComponent />

4. STYLING (Add to your CSS)
   
   .chat-container {
     display: flex;
     flex-direction: column;
     height: 500px;
     border: 1px solid #ccc;
     border-radius: 8px;
     background: #f9f9f9;
   }

   .chat-messages {
     flex: 1;
     overflow-y: auto;
     padding: 16px;
     display: flex;
     flex-direction: column;
     gap: 8px;
   }

   .message {
     padding: 12px;
     border-radius: 6px;
     max-width: 80%;
   }

   .message.user {
     background: #007bff;
     color: white;
     align-self: flex-end;
   }

   .message.assistant {
     background: #e9ecef;
     color: #333;
     align-self: flex-start;
   }

   .message.error {
     background: #f8d7da;
     color: #721c24;
     align-self: flex-start;
   }

   .chat-form {
     display: flex;
     gap: 8px;
     padding: 16px;
     border-top: 1px solid #ccc;
   }

   .chat-form input {
     flex: 1;
     padding: 10px;
     border: 1px solid #ddd;
     border-radius: 4px;
     font-size: 14px;
   }

   .chat-form button {
     padding: 10px 20px;
     background: #007bff;
     color: white;
     border: none;
     border-radius: 4px;
     cursor: pointer;
   }

   .chat-form button:disabled {
     background: #ccc;
     cursor: not-allowed;
   }

5. ENVIRONMENT SETUP
   - For development: Backend runs on http://localhost:8000
   - For production: Update REACT_APP_API_URL to your hosted backend

6. TESTING
   - Make sure backend is running: python main.py
   - Start React dev server: npm run dev
   - Open http://localhost:3000
   - Test the chat!
*/
