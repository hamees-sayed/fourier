#!/bin/bash

# Change directory to the server folder
cd server

# Activate virtual environment
source venv/bin/activate

# Run the server
python app.py &

# Change directory to the client folder
cd ../client

# Run the client
npm run dev
