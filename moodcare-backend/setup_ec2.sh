#!/bin/bash

# EC2 Initial Setup Script for MoodCare Backend
# Run this script on a fresh Ubuntu EC2 instance

echo "🔧 Setting up EC2 instance for MoodCare Backend..."

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y nginx tmux git curl
sudo apt install -y postgresql postgresql-contrib  # Optional for PostgreSQL

# Install Node.js (for frontend build if needed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/moodcare
cd ~/moodcare

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/yourusername/moodcare.git .

# Setup backend
echo "🐍 Setting up Django backend..."
cd moodcare-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "📝 Creating .env file..."
cat > .env << EOL
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4),localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
OPENAI_API_KEY=your-openai-key-here
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=7
CORS_ALLOWED_ORIGINS=http://localhost:3000
EOL

echo "⚠️  Please edit .env file to add your OPENAI_API_KEY"

# Run initial migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Create a superuser account:"
python manage.py createsuperuser

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Setup Nginx (optional)
echo "🌐 Setting up Nginx..."
sudo tee /etc/nginx/sites-available/moodcare > /dev/null << EOL
server {
    listen 80;
    server_name $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4);

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /home/ubuntu/moodcare/moodcare-backend/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/moodcare/moodcare-backend/media/;
    }
}
EOL

# Enable site
sudo ln -sf /etc/nginx/sites-available/moodcare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000
sudo ufw --force enable

# Create systemd service (alternative to tmux)
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/moodcare.service > /dev/null << EOL
[Unit]
Description=MoodCare Django Backend
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/moodcare/moodcare-backend
Environment="PATH=/home/ubuntu/moodcare/moodcare-backend/venv/bin"
ExecStart=/home/ubuntu/moodcare/moodcare-backend/venv/bin/python manage.py runserver 0.0.0.0:8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable moodcare

echo "✅ EC2 setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file to add your API keys"
echo "2. Start the server with: tmux new -s moodcare"
echo "3. In tmux, run: source venv/bin/activate && python manage.py runserver 0.0.0.0:8000"
echo "4. Or use systemd: sudo systemctl start moodcare"
echo ""
echo "🌐 Your server will be accessible at:"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo ""
echo "📝 Remember to:"
echo "- Update security group to allow inbound traffic on ports 80, 443, and 8000"
echo "- Configure your domain name if you have one"
echo "- Set up SSL certificate for HTTPS"