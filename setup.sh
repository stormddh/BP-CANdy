#! /bin/bash
# Setup script to create virtual environment and install dependencies
if [ -d __venv ]; then
	echo "Please rename or delete existing __venv directory"
	exit 1
fi

if [ ! -d __venv ]; then
	python3 -m venv __venv
	if [ $? -ne 0 ]; then
		echo "Cannot create python virtual environment"
		exit 1
	fi
fi

if [ ! -d log ]; then
	mkdir log
fi

source __venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
