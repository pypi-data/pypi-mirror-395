import os
from google import genai
from google.genai import types

def get_response(prompt: str, system_instruction: str = None) -> str:
    """
    Sends a prompt to the Gemini API and returns the generated text response.

    The function requires the GEMINI_API_KEY environment variable to be set.

    Args:
        prompt: The user query string.
        system_instruction: An optional instruction to guide the model's behavior.

    Returns:
        The generated text response as a string, or an error message if the API key is missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: The GEMINI_API_KEY environment variable is not set."

    if not prompt:
        return "Please enter a query."

    try:
        # Initialize the client with the API key
        client = genai.Client(api_key=api_key)

        config = None
        if system_instruction:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )

        # Call the Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config,
        )

        # Basic response formatting
        if response.text.startswith('**') and response.text.endswith('**'):
            return response.text.strip('*')
        return response.text

    except Exception as e:
        return f"An API error occurred: {e}"

def summarize_text(text: str) -> str:
    """
    Summarizes a long piece of text using the get_response function with a specific
    system instruction for summarization.
    """
    summary_prompt = f"Summarize the following text concisely and accurately:\n\n{text}"
    return get_response(summary_prompt, system_instruction="You are an expert summarization tool. Your output must be a single, coherent paragraph.")

# Optional: Add a simple README for documentation