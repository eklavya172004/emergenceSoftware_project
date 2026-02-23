#!/bin/bash
# Database Quick Start Script
# Run from: terminal in VS Code
# Command: bash backend/quickstart.sh

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Database Integration - Quick Start Setup             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print steps
step() {
    echo -e "${BLUE}→${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Step 1: Navigate to backend
step "Navigating to backend directory..."
cd backend 2>/dev/null || { echo "Error: backend directory not found"; exit 1; }
success "Backend directory ready"
echo ""

# Step 2: Check Python environment
step "Checking Python environment..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    success "Python found: $PYTHON_VERSION"
else
    echo "Error: Python not found. Please install Python 3.8+"
    exit 1
fi
echo ""

# Step 3: Activate virtual environment
step "Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
    success "Virtual environment activated"
else
    warning "Virtual environment not found. Creating new one..."
    python -m venv venv
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate
    success "Virtual environment created and activated"
fi
echo ""

# Step 4: Install dependencies
step "Installing/updating dependencies..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt --quiet
    success "Dependencies installed"
else
    echo "Error: pip not found"
    exit 1
fi
echo ""

# Step 5: Initialize database
step "Initializing database..."
if python init_db.py; then
    success "Database initialized successfully"
else
    echo "Error: Database initialization failed"
    exit 1
fi
echo ""

# Step 6: Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   Setup Complete! 🎉                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}What's next?${NC}"
echo ""
echo "1. Start the backend server:"
echo "   python main.py"
echo ""
echo "2. Open API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. Test an endpoint:"
echo "   curl -X POST http://localhost:8000/api/v1/conversations/start \\"
echo "   -H 'Content-Type: application/json' \\"
echo "   -d '{\"user_name\": \"TestUser\"}'"
echo ""
echo "4. Check database connection:"
echo "   curl http://localhost:8000/api/v1/conversations/db-health"
echo ""
echo "5. Read documentation:"
echo "   - DATABASE.md (configuration & schema)"
echo "   - DATABASE_EXAMPLES.py (code examples)"
echo "   - FRONTEND_INTEGRATION.py (React setup)"
echo ""

# Optional: Ask if user wants to start server now
read -p "Start backend server now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting server..."
    python main.py
fi
