#!/bin/bash
# Watermarker installation script for Linux/macOS
# This script installs dependencies and optionally adds watermark to PATH

echo "========================================"
echo "Watermarker Installation Script"
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from your package manager or https://www.python.org/"
    exit 1
fi

echo "Python 3 found!"
echo ""

# Install required packages
echo "Installing required Python packages..."
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt" --user

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Dependencies installed successfully!"
echo ""

# Make the script executable
chmod +x "$SCRIPT_DIR/watermark.py"

# Create a wrapper script in user's local bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    echo "Creating watermark command in ~/.local/bin..."
    cat > "$HOME/.local/bin/watermark" << EOL
#!/bin/bash
python3 "$SCRIPT_DIR/watermark.py" "\$@"
EOL
    chmod +x "$HOME/.local/bin/watermark"
    
    echo ""
    echo "Watermark command installed to ~/.local/bin/watermark"
    echo ""
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "Note: ~/.local/bin is not in your PATH"
        echo "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
    else
        echo "You can now run 'watermark' from anywhere!"
        echo ""
    fi
else
    echo "~/.local/bin does not exist. Creating it..."
    mkdir -p "$HOME/.local/bin"
    
    cat > "$HOME/.local/bin/watermark" << EOL
#!/bin/bash
python3 "$SCRIPT_DIR/watermark.py" "\$@"
EOL
    chmod +x "$HOME/.local/bin/watermark"
    
    echo ""
    echo "Created ~/.local/bin and installed watermark command"
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Usage Examples:"
echo "  watermark --path image.jpg --text \"CONFIDENTIAL\""
echo "  watermark  (for interactive mode)"
echo ""
echo "For more information, run: watermark --help"
echo ""
