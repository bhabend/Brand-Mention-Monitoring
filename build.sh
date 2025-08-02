#!/usr/bin/env bash

# Upgrade pip and essential tools first
python -m pip install --upgrade pip setuptools wheel

# Then install the rest
pip install -r requirements.txt
