import random
import time
import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def get_response(prompt):
    """
    Simulates sending a prompt to the Anti Gravity AI API.
    
    Args:
        prompt (str): The user's input query.
        
    Returns:
        str: The AI-generated response.
    """
    # 1. Check for Real API Key (Environment Variable)
    api_key = os.environ.get("AI_API_KEY")
    
    if api_key:
        # --- REAL API CALL IMPLEMENTATION (Google Gemini) ---
        try:
            return call_gemini_api(prompt, api_key)
        except Exception as e:
            return f"API Error: {str(e)}"
            
    # 2. Simulation Mode (Default)
    # Simulate API latency
    time.sleep(1)
    
    # Mock responses for demonstration
    responses = [
        f"Anti Gravity AI says: That's an interesting question about '{prompt}'. Here is a simulated insight.",
        f"Anti Gravity AI Analysis: '{prompt}' is a complex topic. Let me break it down...",
        f"Response from Anti Gravity Core: I have processed '{prompt}' and found multiple possibilities.",
        "Anti Gravity AI: I am currently in simulation mode, but I can tell you that the future of AI is bright!",
    ]
    
    response = random.choice(responses)
    return format_response(response)

def call_gemini_api(prompt, api_key):
    """
    Calls Google Gemini API.
    """
    if not genai:
        raise ImportError("google-generativeai library is not installed.")
        
    genai.configure(api_key=api_key)
    # Updated model name to available version
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

def summarize_text(text):
    """
    Summarizes the given text.
    
    Args:
        text (str): The text to summarize.
        
    Returns:
        str: A summary of the text.
    """
    if not text:
        return ""
    
    words = text.split()
    if len(words) <= 10:
        return text # Too short to summarize
        
    return " ".join(words[:10]) + "..."

def format_response(text):
    """
    Cleans and formats the text (e.g., removing extra whitespace).
    
    Args:
        text (str): The text to format.
        
    Returns:
        str: The formatted text.
    """
    if not text:
        return ""
    
    return " ".join(text.split())
