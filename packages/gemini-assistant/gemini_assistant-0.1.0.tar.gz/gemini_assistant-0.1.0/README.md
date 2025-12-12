Gemini Assistant Library

gemini_assistant is a simple Python package designed to streamline interactions with the Google Gemini API, making it easy to integrate AI functionality into your applications, such as a Flask web app.

Installation

Clone the repository/Navigate to the directory.

Install locally (simulating PyPI):

pip install .


Usage

Before use, set your API key:

export GEMINI_API_KEY="YOUR_API_KEY_HERE"


Example

from gemini_assistant import get_response

# Basic text generation
query = "Explain the concept of quantum entanglement in simple terms."
ai_output = get_response(query)
print(ai_output)

# Summarization helper
long_text = "..."
summary = summarize_text(long_text)
print(summary)
