#!/bin/bash
# Simple start script for development

echo "🚀 Starting Shopify-WordPress Migrator..."

# Check if Docker Compose is available
if command -v docker-compose &> /dev/null; then
    echo "Starting with Docker Compose..."
    docker-compose up -d
    echo "✅ Application started!"
    echo "Frontend: http://localhost:3000"
    echo "Backend: http://localhost:8000"
    echo "API Docs: http://localhost:8000/api/docs"
else
    echo "Docker Compose not found. Starting manually..."
    
    # Start backend
    echo "Starting backend..."
    cd backend
    if [ ! -d "venv" ]; then
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    uvicorn main:app --reload &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    echo "Starting frontend..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Application started!"
    echo "Backend PID: $BACKEND_PID"
    echo "Frontend PID: $FRONTEND_PID"
    echo ""
    echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
fi

echo ""
echo "📚 Documentation available in README.md"
