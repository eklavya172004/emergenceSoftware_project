'use client';

import React, { FC, useState, useEffect } from 'react';
import Link from 'next/link';

const BotPopup: FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [showMessage, setShowMessage] = useState(false);

  useEffect(() => {
    // Show popup after 2 seconds
    const timer = setTimeout(() => {
      setIsVisible(true);
      setShowMessage(true);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setShowMessage(false);
  };

  return (
    <>
      {isVisible && (
        <div className="fixed bottom-8 right-8 z-50 flex flex-col items-end gap-4">
          {/* Message Popup */}
          {showMessage && (
            <div className="animate-bounce bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 p-[2px] rounded-2xl shadow-lg max-w-xs">
              <div className="bg-[#121212] rounded-2xl p-4 text-white">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">🤖</span>
                  <p className="font-semibold">Resume Assistant</p>
                </div>
                <p className="text-sm text-gray-200 mb-4">
                  Ask me about my resume, skills, projects, and experience!
                </p>
                <div className="flex gap-2">
                  <Link
                    href="/chat"
                    className="flex-1 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 text-center text-sm"
                  >
                    Chat Now
                  </Link>
                  <button
                    onClick={handleClose}
                    className="px-3 py-2 text-gray-400 hover:text-white transition"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Floating Bot Icon */}
          <Link
            href="/chat"
            className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 p-[2px] shadow-lg hover:shadow-cyan-500/50 hover:shadow-2xl transition-all duration-300 hover:scale-110 active:scale-95 flex items-center justify-center"
            title="Chat with AI Assistant"
          >
            <div className="w-full h-full rounded-full bg-[#121212] flex items-center justify-center text-3xl hover:bg-[#1a1a1a] transition">
              💬
            </div>
          </Link>
        </div>
      )}
    </>
  );
};

export default BotPopup;
