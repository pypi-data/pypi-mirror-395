#!/bin/bash
# setup-dev.sh - Linux/Mac development environment setup for prism-view
# Usage: ./setup-dev.sh

set -e

# Colors
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;90m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo ""
echo -e "${MAGENTA}    ██████╗ ██████╗ ██╗███████╗███╗   ███╗${NC}"
echo -e "${MAGENTA}    ██╔══██╗██╔══██╗██║██╔════╝████╗ ████║${NC}"
echo -e "${CYAN}    ██████╔╝██████╔╝██║███████╗██╔████╔██║${NC}"
echo -e "${CYAN}    ██╔═══╝ ██╔══██╗██║╚════██║██║╚██╔╝██║${NC}"
echo -e "${BLUE}    ██║     ██║  ██║██║███████║██║ ╚═╝ ██║${NC}"
echo -e "${BLUE}    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚═╝${NC}"
echo ""
echo -e "${WHITE}    👁️  prism-view Development Setup${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 not found. Please install Python 3.10+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}Found: $PYTHON_VERSION${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${GRAY}Virtual environment already exists, reusing...${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip --quiet

# Install package in editable mode with dev dependencies
echo -e "${YELLOW}Installing prism-view with dev dependencies...${NC}"
pip install -e ".[dev]"

# Verify installation
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"
if python -c "from prism.view import __version__; print(f'prism-view v{__version__}')" 2>/dev/null; then
    echo -e "${GREEN}Installation verified successfully${NC}"
    echo ""
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${GREEN}  Setup complete!${NC}"
    echo -e "${GREEN}==========================================${NC}"
else
    echo ""
    echo -e "${YELLOW}WARNING: Installation may have issues${NC}"
    echo -e "${YELLOW}The package installed but verification failed.${NC}"
    echo -e "${YELLOW}This is expected if __init__.py is not yet complete.${NC}"
fi

echo ""
echo -e "${CYAN}To activate the virtual environment:${NC}"
echo -e "${WHITE}  source .venv/bin/activate${NC}"
echo ""
echo -e "${CYAN}To run tests:${NC}"
echo -e "${WHITE}  pytest${NC}"
echo ""
echo -e "${CYAN}To run tests with coverage:${NC}"
echo -e "${WHITE}  pytest --cov=src/prism/view --cov-report=term-missing${NC}"
echo ""
