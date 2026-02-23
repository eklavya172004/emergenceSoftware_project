#!/usr/bin/env bash
# Quick test script to verify frontend connection

echo "Testing Frontend-Backend Connection"
echo "===================================="
echo ""
echo "Make sure:"
echo "1. Backend is running: python main.py (in backend folder)"
echo "2. Frontend is running: npm run dev (in root folder)"
echo "3. Open http://localhost:3000/chat in your browser"
echo ""
echo "Frontend should:"
echo "✓ Let you enter a name"
echo "✓ Auto-create a conversation"
echo "✓ Enable the message input field"
echo "✓ Let you type and send messages"
echo ""
echo "If still not working, check browser console (F12) for errors"
