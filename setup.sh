#!/bin/bash

echo "🔧 Upgrading pip, setuptools, and wheel"
pip install --upgrade pip setuptools wheel

echo "🚀 Starting Streamlit app"
streamlit run app.py
