#! /bin/bash
# Setup script to create virtual environment and install dependencies

if [ ! -d __venv ]; then
	python3 -m venv __venv
fi
source __venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
