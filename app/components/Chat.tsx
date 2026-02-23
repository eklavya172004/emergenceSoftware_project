'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { api, formatTime, formatDate, Message } from '../lib/api';
import { useToast } from './Toast';
import clsx from 'clsx';

interface Conversation {
  conversation_id: string;
  user_name: string;
  created_at: string;
}

export const Chat: React.FC = () => {
  // Toast
  const { addToast } = useToast();

  // State
  const [userName, setUserName] = useState('');
  const [userNameSubmitted, setUserNameSubmitted] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [conversationPreviews, setConversationPreviews] = useState<Record<string, string>>({});
  const [showHistory, setShowHistory] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch user conversations
  const fetchConversations = async (name: string) => {
    try {
      setError(null);
      const result = await api.getUserConversations(name);
      const convsData = result.conversations || [];
      setConversations(convsData);

      // Fetch previews for all conversations in parallel
      const previews: Record<string, string> = {};
      
      await Promise.all(
        convsData.map(async (conv) => {
          try {
            const history = await api.getConversationHistory(conv.conversation_id);
            const firstUserMessage = history.messages?.find((m) => m.role === 'user');
            if (firstUserMessage) {
              previews[conv.conversation_id] = firstUserMessage.content;
            }
          } catch (err) {
            console.error(`Failed to fetch preview for ${conv.conversation_id}:`, err);
          }
        })
      );
      
      setConversationPreviews(previews);
      return convsData;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to fetch conversations';
      console.error('Failed to fetch conversations:', err);
      setError(errorMsg);
      return [];
    }
  };

  // Handle user name submission
  const handleUserNameSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (userName.trim()) {
      setUserNameSubmitted(true);
      setError(null);
      
      try {
        // Fetch existing conversations
        const existingConversations = await fetchConversations(userName);
        
        // If no conversations exist, auto-create one
        if (existingConversations.length === 0) {
          try {
            const response = await api.startConversation({
              user_name: userName,
            });
            
            if (response.conversation_id) {
              setCurrentConversationId(response.conversation_id);
              setMessages([]);
              setInputValue('');
            }
          } catch (err) {
            console.error('Error creating conversation:', err);
            setError('Failed to create conversation. Try clicking "+ New Chat"');
          }
        }
      } catch (err) {
        console.error('Error during name submission:', err);
        setError('Failed to load conversations');
      }
    }
  };

  // Start new conversation
  const handleNewChat = async () => {
    try {
      setError(null);
      setMessages([]);
      setInputValue('');

      const response = await api.startConversation({
        user_name: userName,
      });

      setCurrentConversationId(response.conversation_id);
      await fetchConversations(userName);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to start conversation'
      );
    }
  };

  // Load conversation
  const handleLoadConversation = async (conversationId: string) => {
    try {
      setError(null);
      setIsLoading(true);

      const history = await api.getConversationHistory(conversationId);
      setMessages(history.messages || []);
      setCurrentConversationId(conversationId);
      setShowHistory(false);
      setInputValue('');
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to load conversation'
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Load latest conversation
  useEffect(() => {
    if (conversations.length > 0 && !currentConversationId) {
      const latest = conversations[0];
      if (latest) {
        handleLoadConversation(latest.conversation_id);
      }
    }
  }, [conversations, currentConversationId]);

  // Delete conversation
  const handleDeleteConversation = async (conversationId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    
    addToast({
      type: 'confirm',
      message: 'Delete this conversation? This action cannot be undone.',
      onConfirm: async () => {
        try {
          await api.deleteConversation(conversationId);
          await fetchConversations(userName);
          if (currentConversationId === conversationId) {
            setMessages([]);
            setCurrentConversationId(null);
          }
          addToast({
            type: 'success',
            message: 'Conversation deleted successfully',
            duration: 2000,
          });
        } catch (err) {
          addToast({
            type: 'error',
            message: err instanceof Error ? err.message : 'Failed to delete conversation',
            duration: 3000,
          });
        }
      },
    });
  };

  // Send message
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !currentConversationId) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setError(null);
    setIsLoading(true);

    // Add user message to UI immediately
    const newMessage: Message = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newMessage]);

    try {
      const response = await api.sendMessage({
        message: userMessage,
        conversation_id: currentConversationId,
        conversation_history: messages,
      });

      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp || new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to send message'
      );
      // Remove the user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  // Not logged in
  if (!userNameSubmitted) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0a0e27]">
        <div className="w-full max-w-md mx-auto px-6">
          <div className="bg-gradient-to-br from-[#1a1f3a] to-[#0f1219] rounded-2xl p-8 border border-[#2a3f5f]">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
              Chat Assistant
            </h1>
            <p className="text-gray-400 mb-8">
              Ask questions about my resume and experience
            </p>

            <form onSubmit={handleUserNameSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Your Name
                </label>
                <input
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  placeholder="Enter your name"
                  className="w-full px-4 py-3 bg-[#0f1219] border border-[#2a3f5f] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition"
                  autoFocus
                />
              </div>
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-3 rounded-lg transition transform hover:scale-105"
              >
                Start Chat
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  // Chat interface
  return (
    <div className="flex h-screen bg-[#0a0e27]">
      {/* Sidebar */}
      <aside
        className={clsx(
          'bg-gradient-to-b from-[#0f1219] to-[#0a0e27] border-r border-[#2a3f5f] transition-all duration-300 flex flex-col shadow-2xl',
          isSidebarOpen ? 'w-72' : 'w-0 overflow-hidden'
        )}
      >
        {/* Sidebar Header */}
        <div className="p-4 border-b border-[#2a3f5f] bg-[#1a1f3a]/50 backdrop-blur">
          <div className="flex items-center gap-2 mb-2 justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">👋</span>
              <h2 className="text-white font-bold text-lg">Hi, {userName}!</h2>
            </div>
            <Link
              href="/"
              className="text-2xl hover:scale-110 transition-transform duration-200 flex items-center justify-center w-9 h-9 rounded-lg hover:bg-blue-500/20"
              title="Go to home page"
            >
              🏠
            </Link>
          </div>
          <div className="flex items-center justify-between text-xs">
            <p className="text-gray-400">
              💬 {conversations.length} conversation{conversations.length !== 1 ? 's' : ''}
            </p>
            <span className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded-full text-xs font-medium">
              {conversations.length}
            </span>
          </div>
        </div>

        {/* New Chat Button */}
        <button
          onClick={handleNewChat}
          className="m-4 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-500 via-cyan-500 to-blue-600 hover:from-blue-600 hover:via-cyan-600 hover:to-blue-700 text-white font-bold py-3 rounded-xl transition duration-200 shadow-lg hover:shadow-blue-500/50 hover:shadow-xl active:scale-95"
        >
          <span className="text-lg">✨</span>
          + New Chat
          <span className="text-lg">💬</span>
        </button>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto px-3 space-y-2">
          {conversations.length === 0 ? (
            <p className="text-center text-gray-400 text-sm py-8">
              <div className="text-2xl mb-2">💬</div>
              No conversations yet
            </p>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.conversation_id}
                onClick={() => handleLoadConversation(conv.conversation_id)}
                className={clsx(
                  'p-3 rounded-xl cursor-pointer transition group border-2 hover:shadow-lg',
                  currentConversationId === conv.conversation_id
                    ? 'bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border-blue-500 shadow-lg'
                    : 'bg-[#1a1f3a] border-[#2a3f5f] hover:bg-[#202537] hover:border-[#3a5f7f]'
                )}
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-2">
                  <p className="text-sm font-semibold text-white">
                    💭 {conv.user_name}
                  </p>
                  <button
                    onClick={(e) => handleDeleteConversation(conv.conversation_id, e)}
                    className="text-red-400 hover:text-red-300 opacity-0 group-hover:opacity-100 transition text-xs hover:bg-red-500/20 px-2 py-1 rounded"
                    title="Delete conversation"
                  >
                    ✕
                  </button>
                </div>

                {/* Timestamp */}
                <p className="text-xs text-gray-400 mb-2">
                  📅 {formatDate(conv.created_at)}
                </p>

                {/* Message Preview */}
                {conversationPreviews[conv.conversation_id] && (
                  <p className="text-xs text-gray-300 line-clamp-2 bg-[#0f1219]/50 rounded px-2 py-2 border-l-2 border-blue-400">
                    <span className="text-gray-500">Q: </span>
                    {conversationPreviews[conv.conversation_id]}
                  </p>
                )}
              </div>
            ))
          )}
        </div>

        <div className="p-4 border-t border-[#2a3f5f]">
          <button
            onClick={() => {
              setUserNameSubmitted(false);
              setMessages([]);
              setCurrentConversationId(null);
            }}
            className="w-full text-sm text-gray-400 hover:text-gray-300 py-2 transition"
          >
            Change User
          </button>
        </div>
      </aside>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-gradient-to-b from-[#0a0e27] to-[#0f1219]">
        {/* Header */}
        <header className="bg-gradient-to-r from-[#1a1f3a] to-[#0f1219] border-b border-[#2a3f5f] px-6 py-5 flex items-center justify-between shadow-lg">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="text-gray-400 hover:text-white transition md:hidden text-2xl hover:bg-[#2a3f5f]/50 p-2 rounded-lg"
            title="Toggle sidebar"
          >
            ☰
          </button>
          <div className="flex-1 text-center">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500 bg-clip-text text-transparent">
              🤖 AI Resume Assistant
            </h1>
            <p className="text-xs text-gray-400 mt-1">Ask questions about my experience and skills</p>
          </div>
          <div className="w-6 h-6" />
        </header>

        {/* Messages Container */}
        <main className="flex-1 overflow-y-auto p-6 space-y-4 scroll-smooth">
          {messages.length === 0 && !isLoading ? (
            <div className="flex items-center justify-center h-full text-center">
              <div className="max-w-sm">
                <div className="text-7xl mb-6 animate-bounce">💬</div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-3">
                  Start a conversation!
                </h2>
                <p className="text-gray-400 text-lg leading-relaxed">
                  Ask me anything about my resume, technical skills, projects, experience, or background.
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={clsx(
                    'flex gap-3 mb-2',
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  )}
                >
                  {message.role === 'assistant' && (
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center text-sm flex-shrink-0">
                      🤖
                    </div>
                  )}
                  <div
                    className={clsx(
                      'max-w-xs lg:max-w-2xl px-5 py-3 rounded-2xl shadow-md',
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-blue-600 to-blue-500 text-white rounded-br-none backdrop-blur-sm'
                        : 'bg-[#1a2540] text-gray-100 rounded-bl-none border border-[#3a5f7f]/50 backdrop-blur-sm'
                    )}
                  >
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    {message.timestamp && (
                      <p
                        className={clsx(
                          'text-xs mt-2 font-medium',
                          message.role === 'user'
                            ? 'text-blue-100 opacity-75'
                            : 'text-gray-500'
                        )}
                      >
                        {formatTime(message.timestamp)}
                      </p>
                    )}
                  </div>
                  {message.role === 'user' && (
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-cyan-400 flex items-center justify-center text-sm flex-shrink-0">
                      👤
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center text-sm flex-shrink-0">
                    🤖
                  </div>
                  <div className="bg-[#1a2540] text-gray-100 rounded-2xl rounded-bl-none border border-[#3a5f7f]/50 px-5 py-3 shadow-md">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-200" />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </main>

        {/* Error Message */}
        {error && (
          <div className="px-6 py-4 bg-gradient-to-r from-red-900/40 to-red-800/40 border-t border-red-700/50 backdrop-blur-sm">
            <div className="flex items-center gap-3">
              <span className="text-xl">⚠️</span>
              <p className="text-sm text-red-300 font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Input Area */}
        <form
          onSubmit={handleSendMessage}
          className="border-t border-[#2a3f5f] bg-gradient-to-t from-[#0a0e27] to-[#0f1219] p-5 shadow-2xl"
        >
          <div className="flex gap-3 items-stretch">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage(e as any);
                }
              }}
              placeholder={!currentConversationId ? "Start a conversation first..." : "Ask me about my skills, projects, or experience..."}
              disabled={!currentConversationId || isLoading}
              className="flex-1 px-5 py-3 bg-[#1a2540]/80 border-2 border-[#2a5f7f] rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:bg-[#1a2540] transition disabled:opacity-40 disabled:cursor-not-allowed backdrop-blur-sm"
            />
            <button
              type="submit"
              disabled={!currentConversationId || isLoading || !inputValue.trim()}
              className="bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600 hover:from-blue-700 hover:via-cyan-600 hover:to-blue-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold px-6 py-3 rounded-xl transition duration-200 shadow-lg hover:shadow-cyan-500/50 hover:shadow-xl active:scale-95 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <span className="animate-spin">⚡</span>
                  Thinking...
                </>
              ) : (
                <>
                  <span>📤</span>
                  Send
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chat;
