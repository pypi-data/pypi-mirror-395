# iai-helper — Intelligent AI Helper

A super-fast, clean and simple Python wrapper for Groq's blazing-fast LLMs.  
Created and published on PyPI as part of my AI-Powered Web Assistant college project (Dec 2025).

```bash
pip install iai-helper

PyPI version
Python
Downloads
License
Features

One-line AI chat using Groq (fastest inference available)
Automatic GROQ_API_KEY loading from environment
Built-in response cleaning
Perfect for Flask, FastAPI, Streamlit, scripts, etc.

Quick Start
Pythonfrom iai_helper import IAIHelper

ai = IAIHelper()  # Automatically uses your GROQ_API_KEY
print(ai.ask("Write a beautiful poem about the ocean"))
Get Your Free Groq API Key (30 seconds)

Go to → https://console.groq.com/keys
Sign up / log in
Copy your key → set as environment variable:

Bashexport GROQ_API_KEY="gsk_your_key_here"
Or create .env file:
textGROQ_API_KEY=gsk_your_key_here
Example Usage
Pythonfrom iai_helper import IAIHelper, clean_response

ai = IAIHelper()

response = ai.ask("Explain quantum physics like I'm 12")
print(clean_response(response))

Used In
This package powers my full-stack AI Web Assistant built with Flask + Bootstrap + SweetAlert.

Author
Akash Sabu
December 2025