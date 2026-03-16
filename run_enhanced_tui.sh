#!/bin/bash
# Script to run the enhanced TUI with virtual environment

# Activate virtual environment
source venv/bin/activate

# Run the app
python random_gen.py

# Deactivate when done
deactivate
