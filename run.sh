#!/bin/bash

# Change directory to the server folder
cd server

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    # Create virtual environment if it doesn't exist
    python3 -m venv venv
    source venv/bin/activate
    # Install requirements
    pip install -r requirements.txt
else
    # Activate virtual environment
    source venv/bin/activate
fi

# Run the server
python app.py &

# Change directory back to the client folder
cd ../client

# Check if node_modules folder exists
if [ ! -d "node_modules" ]; then
    # Install npm packages
    npm install
fi

# Run the client
npm run dev
