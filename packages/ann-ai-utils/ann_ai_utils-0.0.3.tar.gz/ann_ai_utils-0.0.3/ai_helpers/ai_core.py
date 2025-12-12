import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# Load environment variables from .env file
load_dotenv()
# The 'google-genai' library automatically looks for the GEMINI_API_KEY environment variable.

def get_response(prompt):
    """
    Send a prompt to the Gemini API and return the response text.
    The API key is automatically loaded from the GEMINI_API_KEY environment variable.
    """
    try:
        # Initialize the client. It will automatically look for GEMINI_API_KEY
        # in the environment variables.
        client = genai.Client()
        
        # Specify the model and configuration
        model_name = 'gemini-2.5-flash'  # A good, fast model for general tasks
        
        # Generate the content
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                'max_output_tokens': 200  # Sets the max response length
            }
        )
        
        return response.text
        
    except APIError as e:
        print(f"Gemini API Error: {e}")
        return "Error: Could not retrieve response from the Gemini API."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Error: An unexpected error occurred."


def summarize_text(text):
    """Return a short summary."""
    # Ensure text is long enough before slicing
    if len(text) > 100:
        return text[:100] + "..."
    return text


def format_response(text):
    """Clean whitespace and formatting."""
    return text.strip()


# --- Example Usage ---
# NOTE: You must have a .env file in the same directory with your key:
# GEMINI_API_KEY="YOUR_API_KEY_HERE"

if __name__ == '__main__':
    # You need to install the required libraries:
    # pip install google-genai python-dotenv
    
    # Check if the API key is loaded
    if os.getenv("GEMINI_API_KEY"):
        print("Gemini API Key loaded. Sending prompt...")
        
        test_prompt = "Explain the concept of quantum entanglement in simple terms."
        ai_response = get_response(test_prompt)
        
        formatted_result = format_response(ai_response)
        summary = summarize_text(formatted_result)
        
        print("\n--- Original Prompt ---")
        print(test_prompt)
        print("\n--- Full AI Response ---")
        print(formatted_result)
        print("\n--- Summary ---")
        print(summary)
    else:
        print("Error: GEMINI_API_KEY not found. Please create a .env file and add your key.")