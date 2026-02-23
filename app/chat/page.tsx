'use client';

import { FC } from 'react';
import Chat from '../components/Chat';
import { ToastProvider } from '../components/Toast';

const ChatPage: FC = () => {
  return (
    <ToastProvider>
      <main className="w-full h-screen">
        <Chat />
      </main>
    </ToastProvider>
  );
};

export default ChatPage;
