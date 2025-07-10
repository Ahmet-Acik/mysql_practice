#!/bin/bash

# Environment Configuration Helper
# Helps users set up the correct environment configuration

echo "🔧 MySQL Practice Project - Environment Setup"
echo "=============================================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists."
    read -p "Do you want to reconfigure it? (y/N): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Using existing .env file."
        exit 0
    fi
fi

echo "Please choose your setup:"
echo "1. Docker (recommended) - Uses containerized MySQL on port 3307"
echo "2. Local MySQL - Uses your existing MySQL installation on port 3306"
echo "3. Custom configuration"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🐳 Setting up Docker configuration..."
        cp .env.example .env
        echo "✅ Docker configuration ready!"
        echo ""
        echo "Next steps:"
        echo "  make docker-setup    # Start Docker environment"
        echo "  make docker-mysql    # Access MySQL shell"
        echo "  📍 phpMyAdmin: http://localhost:8080"
        ;;
    2)
        echo "🏠 Setting up local MySQL configuration..."
        cp .env.example .env
        sed -i '' 's/DB_HOST=mysql/DB_HOST=localhost/' .env
        sed -i '' 's/DB_PORT=3306/DB_PORT=3306/' .env
        sed -i '' 's/DB_USER=practice_user/DB_USER=root/' .env
        sed -i '' 's/DB_PASSWORD=practice_password/DB_PASSWORD=/' .env
        
        echo "📝 Please edit .env file with your MySQL credentials:"
        echo "  - Update DB_USER with your MySQL username"
        echo "  - Update DB_PASSWORD with your MySQL password"
        echo ""
        read -p "Do you want to edit .env now? (Y/n): " -r
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            ${EDITOR:-nano} .env
        fi
        
        echo "✅ Local MySQL configuration ready!"
        echo ""
        echo "Next steps:"
        echo "  make setup          # Initialize database"
        echo "  make examples       # Run examples"
        ;;
    3)
        echo "⚙️  Setting up custom configuration..."
        cp .env.example .env
        echo "📝 Please edit .env file with your custom settings:"
        ${EDITOR:-nano} .env
        echo "✅ Custom configuration ready!"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🧪 Testing database connection..."
if python -c "from config.database import test_connection; print('✅ Connection successful!' if test_connection() else '❌ Connection failed!')" 2>/dev/null; then
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Try these commands:"
    echo "  python cli.py        # Interactive mode"
    echo "  make examples        # Run examples"
    echo "  make help           # See all commands"
else
    echo "⚠️  Connection test failed. Please check your configuration."
    echo "You can edit .env file manually or run this script again."
fi
