#!/bin/bash

echo "===== NeuroLink: Cyberpunk Data Recovery ====="
echo "Installing dependencies and setting up the game..."

# Create virtual environment
python3 -m venv neurolink-env

# Activate virtual environment
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source neurolink-env/bin/activate
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source neurolink-env/Scripts/activate
else
    echo "Could not detect OS type for activation. Please activate the virtual environment manually."
    exit 1
fi

# Install requirements
pip install -r requirements.txt

echo "===== Installation Complete ====="
echo "To play the game:"
echo "1. Activate the virtual environment if not already activated"
echo "   source neurolink-env/bin/activate  (macOS/Linux)"
echo "   neurolink-env\\Scripts\\activate  (Windows)"
echo "2. Run the game: python neurolink.py"
echo ""
echo "Enjoy your cyberpunk adventure!"
