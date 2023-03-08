#!/bin/bash
# create virtual environment
python3 -m venv venv
# activate virtual environment
source venv/bin/activate
# upgrade pip
pip install --upgrade pip
# install requirements in virtual environment
pip install -r requirements.txt
