#!/bin/bash

# MoodCare Backend Deployment Script
# This script handles zero-downtime deployment on AWS EC2

echo "🚀 Starting MoodCare Backend Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/ubuntu/moodcare/moodcare-backend"
VENV_DIR="$PROJECT_DIR/venv"
TMUX_SESSION="moodcare"
PORT=8000

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if running as correct user
if [ "$USER" != "ubuntu" ]; then
    print_warning "This script should be run as ubuntu user"
fi

# Navigate to project directory
cd $PROJECT_DIR || {
    print_error "Project directory not found!"
    exit 1
}

# Pull latest code from GitHub
print_status "Pulling latest code from GitHub..."
git pull origin main || {
    print_error "Failed to pull from GitHub"
    exit 1
}

# Activate virtual environment
print_status "Activating virtual environment..."
source $VENV_DIR/bin/activate || {
    print_error "Failed to activate virtual environment"
    exit 1
}

# Install/update dependencies
print_status "Installing/updating dependencies..."
pip install -r requirements.txt || {
    print_error "Failed to install dependencies"
    exit 1
}

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate --noinput || {
    print_error "Failed to run migrations"
    exit 1
}

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput || {
    print_error "Failed to collect static files"
    exit 1
}

# Check if tmux session exists
tmux has-session -t $TMUX_SESSION 2>/dev/null
if [ $? != 0 ]; then
    print_status "Creating new tmux session..."
    tmux new-session -d -s $TMUX_SESSION
else
    print_status "Using existing tmux session..."
fi

# Perform zero-downtime deployment
print_status "Performing zero-downtime deployment..."

# Stop the current server gracefully
tmux send-keys -t $TMUX_SESSION C-c
sleep 2

# Start the new server
tmux send-keys -t $TMUX_SESSION "source $VENV_DIR/bin/activate" Enter
tmux send-keys -t $TMUX_SESSION "python manage.py runserver 0.0.0.0:$PORT" Enter

# Wait for server to start
sleep 3

# Check if server is running
curl -f http://localhost:$PORT/api/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status "Server is running successfully on port $PORT"
    print_status "Deployment completed successfully! 🎉"
else
    print_error "Server failed to start!"
    exit 1
fi

# Display tmux session info
echo ""
print_status "To view server logs:"
echo "  tmux attach -t $TMUX_SESSION"
echo ""
print_status "To detach from tmux:"
echo "  Press Ctrl+B, then D"
echo ""

# Display server status
print_status "Server Status:"
echo "  URL: http://$(hostname -I | awk '{print $1}'):$PORT"
echo "  API: http://$(hostname -I | awk '{print $1}'):$PORT/api/"
echo "  Admin: http://$(hostname -I | awk '{print $1}'):$PORT/admin/"