#!/usr/bin/env bash
# Shell completion installation script for aws-bedrock-cost-tool
# Generated with Claude Code

set -e

SCRIPT_NAME="aws-bedrock-cost-tool"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}AWS Bedrock Cost Tool - Shell Completion Installer${NC}"
echo ""

# Detect shell
if [ -n "$BASH_VERSION" ]; then
    SHELL_TYPE="bash"
    RC_FILE="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_TYPE="zsh"
    RC_FILE="$HOME/.zshrc"
else
    echo -e "${RED}Error: Unsupported shell${NC}"
    echo "This script supports bash and zsh only."
    exit 1
fi

echo -e "Detected shell: ${GREEN}$SHELL_TYPE${NC}"
echo -e "Configuration file: ${GREEN}$RC_FILE${NC}"
echo ""

# Generate completion script
if [ "$SHELL_TYPE" = "bash" ]; then
    COMPLETION_LINE="eval \"\$(_AWS_BEDROCK_COST_TOOL_COMPLETE=bash_source aws-bedrock-cost-tool)\""
elif [ "$SHELL_TYPE" = "zsh" ]; then
    COMPLETION_LINE="eval \"\$(_AWS_BEDROCK_COST_TOOL_COMPLETE=zsh_source aws-bedrock-cost-tool)\""
fi

# Check if already installed
if grep -q "$COMPLETION_LINE" "$RC_FILE" 2>/dev/null; then
    echo -e "${YELLOW}Completion already installed in $RC_FILE${NC}"
    echo ""
    echo "To activate in current shell, run:"
    echo -e "${GREEN}source $RC_FILE${NC}"
    exit 0
fi

# Add completion to RC file
echo "# aws-bedrock-cost-tool shell completion" >> "$RC_FILE"
echo "$COMPLETION_LINE" >> "$RC_FILE"

echo -e "${GREEN}✓${NC} Completion installed successfully!"
echo ""
echo "To activate in current shell, run:"
echo -e "${GREEN}source $RC_FILE${NC}"
echo ""
echo "Or restart your terminal."
