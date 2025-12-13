#!/bin/bash

# Memory Hub MCP Server - Docker Management Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Main script
case "${1:-help}" in
    "start")
        print_status "Starting Memory Hub MCP Server..."
        check_docker
        
        # Check if LM Studio is accessible
        if ! curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
            print_warning "LM Studio (localhost:1234) is not accessible. Make sure it's running."
            print_warning "The Memory Hub will start but may fail to process requests."
        fi
        
        docker-compose up -d
        print_success "Memory Hub started! Services:"
        echo "  • Memory Hub API: http://localhost:8000"
        echo "  • Qdrant Dashboard: http://localhost:6333/dashboard"
        echo "  • Health Check: http://localhost:8000/health"
        ;;
        
    "stop")
        print_status "Stopping Memory Hub MCP Server..."
        docker-compose down
        print_success "Memory Hub stopped."
        ;;
        
    "restart")
        print_status "Restarting Memory Hub MCP Server..."
        docker-compose down
        docker-compose up -d
        print_success "Memory Hub restarted."
        ;;
        
    "rebuild")
        print_status "Rebuilding and restarting Memory Hub..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        print_success "Memory Hub rebuilt and started."
        ;;
        
    "logs")
        print_status "Showing logs (press Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
        
    "status")
        print_status "Memory Hub Status:"
        docker-compose ps
        echo ""
        print_status "Health Checks:"
        echo -n "Memory Hub API: "
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "✓ Healthy"
        else
            print_error "✗ Unhealthy"
        fi
        
        echo -n "Qdrant: "
        if curl -s http://localhost:6333/health > /dev/null 2>&1; then
            print_success "✓ Healthy"
        else
            print_error "✗ Unhealthy"
        fi
        
        echo -n "LM Studio: "
        if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
            print_success "✓ Accessible"
        else
            print_warning "⚠ Not accessible"
        fi
        ;;
        
    "clean")
        print_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            print_status "Cleaning up Memory Hub..."
            docker-compose down -v --remove-orphans
            docker system prune -f
            print_success "Cleanup completed."
        else
            print_status "Cleanup cancelled."
        fi
        ;;
        
    "reset")
        print_status "Stopping and removing Memory Hub containers (keeping data)..."
        docker-compose down
        docker-compose rm -f
        print_success "Containers removed. Use 'start' to recreate."
        ;;
        
    "debug")
        print_status "Debug information:"
        echo ""
        echo "=== Docker Status ==="
        docker-compose ps
        echo ""
        echo "=== Port Usage ==="
        echo "Port 6333 (Qdrant):"
        lsof -i :6333 || echo "  Port 6333 is free"
        echo "Port 8000 (Memory Hub):"
        lsof -i :8000 || echo "  Port 8000 is free"
        echo ""
        echo "=== Recent Container Logs ==="
        docker-compose logs --tail=20
        ;;
        
    "dev")
        print_status "Starting Memory Hub in development mode..."
        check_docker
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
        print_success "Development mode started with hot reloading."
        ;;
        
    "help"|*)
        echo -e "${BLUE}Memory Hub MCP Server - Docker Management${NC}"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  start     Start the Memory Hub services"
        echo "  stop      Stop the Memory Hub services"
        echo "  restart   Restart the Memory Hub services"
        echo "  rebuild   Rebuild and restart (use after code changes)"
        echo "  logs      Show live logs from all services"
        echo "  status    Show status and health of all services"
        echo "  reset     Stop and remove containers (keep data)"
        echo "  clean     Remove all containers and data (destructive!)"
        echo "  debug     Show detailed debug information"
        echo "  dev       Start in development mode with hot reloading"
        echo "  help      Show this help message"
        echo ""
        echo -e "${YELLOW}Quick Start:${NC}"
        echo "  1. Make sure LM Studio is running on localhost:1234"
        echo "  2. Run: $0 start"
        echo "  3. Check: $0 status"
        ;;
esac 