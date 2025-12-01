#!/bin/bash
# Server setup script for Ubuntu 22.04 LTS
# Run as root or with sudo

set -e

echo "🚀 Starting server setup for VetClinic..."

# Update system
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y

# Install required packages
echo "📦 Installing required packages..."
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
apt-get install -y docker-compose-plugin

# Create deploy user
echo "👤 Creating deploy user..."
if ! id "deploy" &>/dev/null; then
    useradd -m -s /bin/bash deploy
    usermod -aG docker deploy
    echo "deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx" >> /etc/sudoers.d/deploy
fi

# Create project directory
echo "📁 Creating project directory..."
mkdir -p /opt/vetclinic
chown deploy:deploy /opt/vetclinic

# Configure firewall
echo "🔥 Configuring firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# Configure Nginx
echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/vetclinic << 'NGINX_CONFIG'
server {
    listen 80;
    server_name _;  # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        client_max_body_size 20M;
    }
}
NGINX_CONFIG

# Enable the site
ln -sf /etc/nginx/sites-available/vetclinic /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t && systemctl reload nginx

echo ""
echo "✅ Server setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Clone the repository as deploy user:"
echo "   sudo -u deploy git clone https://github.com/YOUR_USERNAME/vetirinary.git /opt/vetclinic"
echo ""
echo "2. Create production environment file:"
echo "   sudo -u deploy cp /opt/vetclinic/.env.example /opt/vetclinic/.env.prod"
echo "   sudo -u deploy nano /opt/vetclinic/.env.prod"
echo ""
echo "3. Generate SSH key for GitHub Actions:"
echo "   sudo -u deploy ssh-keygen -t ed25519 -C 'github-actions' -f /home/deploy/.ssh/github_deploy -N ''"
echo "   cat /home/deploy/.ssh/github_deploy.pub >> /home/deploy/.ssh/authorized_keys"
echo ""
echo "4. Set up SSL (replace YOUR_DOMAIN):"
echo "   certbot --nginx -d YOUR_DOMAIN"
echo ""
echo "5. Start the application:"
echo "   cd /opt/vetclinic && docker-compose -f docker-compose.prod.yml up -d"

