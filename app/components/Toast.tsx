'use client';

import React, { useState, useEffect } from 'react';
import clsx from 'clsx';

export interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning' | 'confirm';
  duration?: number;
  onConfirm?: () => void;
  onCancel?: () => void;
  action?: string;
}

interface ToastContextType {
  toasts: ToastMessage[];
  addToast: (toast: Omit<ToastMessage, 'id'>) => string;
  removeToast: (id: string) => void;
}

export const ToastContext = React.createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = (toast: Omit<ToastMessage, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newToast: ToastMessage = { ...toast, id };
    setToasts((prev) => [...prev, newToast]);

    if (toast.type !== 'confirm' && toast.duration !== 0) {
      setTimeout(() => removeToast(id), toast.duration || 3000);
    }

    return id;
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
      <ToastContainer />
    </ToastContext.Provider>
  );
};

const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useToast();

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-3 pointer-events-none max-w-sm">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onClose={() => removeToast(toast.id)} />
      ))}
    </div>
  );
};

interface ToastItemProps {
  toast: ToastMessage;
  onClose: () => void;
}

const ToastItem: React.FC<ToastItemProps> = ({ toast, onClose }) => {
  const getIcon = () => {
    switch (toast.type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      case 'info':
        return 'ℹ';
      case 'confirm':
        return '❓';
      default:
        return '•';
    }
  };

  const getColors = () => {
    switch (toast.type) {
      case 'success':
        return 'bg-gradient-to-r from-green-600/90 to-emerald-600/90 border-green-500/50 text-green-50';
      case 'error':
        return 'bg-gradient-to-r from-red-600/90 to-red-700/90 border-red-500/50 text-red-50';
      case 'warning':
        return 'bg-gradient-to-r from-amber-600/90 to-orange-600/90 border-amber-500/50 text-amber-50';
      case 'info':
        return 'bg-gradient-to-r from-blue-600/90 to-cyan-600/90 border-blue-500/50 text-blue-50';
      case 'confirm':
        return 'bg-gradient-to-r from-purple-600/90 to-blue-600/90 border-purple-500/50 text-purple-50';
      default:
        return 'bg-gradient-to-r from-gray-600/90 to-gray-700/90 border-gray-500/50 text-gray-50';
    }
  };

  return (
    <div
      className={clsx(
        'pointer-events-auto flex items-start gap-3 p-4 rounded-xl border-2 backdrop-blur-md shadow-lg animate-in fade-in slide-in-from-right-4 duration-300',
        getColors()
      )}
    >
      <span className="text-xl flex-shrink-0 pt-0.5">{getIcon()}</span>

      <div className="flex-1 pt-0.5">
        <p className="text-sm font-semibold leading-tight">{toast.message}</p>
      </div>

      {toast.type === 'confirm' ? (
        <div className="flex gap-2 flex-shrink-0">
          <button
            onClick={() => {
              toast.onConfirm?.();
              onClose();
            }}
            className="px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded-lg text-xs font-bold transition duration-200 backdrop-blur-sm border border-white/20 hover:border-white/40"
          >
            Yes
          </button>
          <button
            onClick={() => {
              toast.onCancel?.();
              onClose();
            }}
            className="px-3 py-1.5 bg-white/10 hover:bg-white/20 rounded-lg text-xs font-bold transition duration-200 backdrop-blur-sm border border-white/20 hover:border-white/30"
          >
            No
          </button>
        </div>
      ) : (
        <button
          onClick={onClose}
          className="text-lg leading-none opacity-70 hover:opacity-100 transition flex-shrink-0 pt-0.5"
        >
          ×
        </button>
      )}
    </div>
  );
};
