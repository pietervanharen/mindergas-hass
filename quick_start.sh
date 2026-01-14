#!/bin/bash

# MinderGas Integration Docker Quick Start
# This script helps you quickly set up and test the integration

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  MinderGas Integration - Docker Quick Start for macOS         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker found"

# Check if docker-compose exists
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed${NC}"
    echo "It should be included with Docker Desktop. Try: docker compose --version"
    exit 1
fi

echo -e "${GREEN}✓${NC} docker-compose found"

# Check if docker daemon is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    echo "Please start Docker Desktop from Applications folder"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker daemon is running"
echo ""

# Main menu
while true; do
    echo -e "${BLUE}What would you like to do?${NC}"
    echo ""
    echo "1) Start Home Assistant (first time setup)"
    echo "2) View Home Assistant logs"
    echo "3) Stop Home Assistant"
    echo "4) Restart Home Assistant"
    echo "5) Test integration (quick checks)"
    echo "6) Clean up (remove all data)"
    echo "7) Show status"
    echo "8) Exit"
    echo ""
    read -p "Enter your choice (1-8): " choice

    case $choice in
        1)
            echo ""
            echo -e "${BLUE}Starting Home Assistant...${NC}"
            docker-compose up -d
            echo -e "${GREEN}✓${NC} Home Assistant starting..."
            echo ""
            echo "Waiting for initialization (this takes 2-3 minutes)..."
            sleep 5
            
            # Show status
            docker-compose ps
            echo ""
            echo -e "${GREEN}✓${NC} Home Assistant is starting!"
            echo ""
            echo "Access at: ${BLUE}http://localhost:8123${NC}"
            echo ""
            echo "Setup steps:"
            echo "1. Complete the Home Assistant setup wizard"
            echo "2. Go to Settings → Devices & Services → Integrations"
            echo "3. Create Integration → Search 'MinderGas'"
            echo "4. Enter your MinderGas API key"
            echo ""
            ;;
        2)
            echo ""
            echo -e "${BLUE}Showing live logs (Ctrl+C to exit)...${NC}"
            docker-compose logs -f home-assistant
            ;;
        3)
            echo ""
            echo -e "${BLUE}Stopping Home Assistant...${NC}"
            docker-compose down
            echo -e "${GREEN}✓${NC} Home Assistant stopped"
            echo ""
            ;;
        4)
            echo ""
            echo -e "${BLUE}Restarting Home Assistant...${NC}"
            docker-compose restart home-assistant
            echo -e "${GREEN}✓${NC} Home Assistant restarted"
            echo ""
            ;;
        5)
            echo ""
            echo -e "${BLUE}Running integration checks...${NC}"
            echo ""
            
            # Check files
            files=(
                "custom_components/mindergas/__init__.py"
                "custom_components/mindergas/api.py"
                "custom_components/mindergas/config_flow.py"
                "custom_components/mindergas/manifest.json"
                "custom_components/mindergas/sensor.py"
            )
            
            all_ok=true
            for file in "${files[@]}"; do
                if [ -f "$file" ]; then
                    echo -e "${GREEN}✓${NC} $file"
                else
                    echo -e "${RED}❌${NC} $file missing"
                    all_ok=false
                fi
            done
            
            echo ""
            
            # Check container
            if docker-compose ps home-assistant | grep -q "Up"; then
                echo -e "${GREEN}✓${NC} Home Assistant is running"
            else
                echo -e "${YELLOW}⚠${NC} Home Assistant is not running (start it with option 1)"
            fi
            
            echo ""
            
            if [ "$all_ok" = true ]; then
                echo -e "${GREEN}✓ All checks passed!${NC}"
                echo ""
                echo "Next steps:"
                echo "1. If not running, start Home Assistant (option 1)"
                echo "2. Visit http://localhost:8123"
                echo "3. Complete setup wizard"
                echo "4. Add MinderGas integration"
            fi
            
            echo ""
            ;;
        6)
            echo ""
            read -p "Are you sure? This will delete all Home Assistant data (y/n): " confirm
            if [ "$confirm" = "y" ]; then
                echo -e "${BLUE}Cleaning up...${NC}"
                docker-compose down -v
                rm -rf home_assistant_data
                echo -e "${GREEN}✓${NC} All data removed"
            else
                echo "Cancelled"
            fi
            echo ""
            ;;
        7)
            echo ""
            echo -e "${BLUE}Home Assistant Status:${NC}"
            docker-compose ps
            echo ""
            
            if docker-compose ps home-assistant | grep -q "Up"; then
                echo -e "${GREEN}✓${NC} Home Assistant is running at http://localhost:8123"
            else
                echo -e "${YELLOW}⚠${NC} Home Assistant is not running"
            fi
            
            echo ""
            ;;
        8)
            echo ""
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please enter 1-8.${NC}"
            echo ""
            ;;
    esac
done
