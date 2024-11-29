import ollama
import requests
from io import BytesIO
import os
import socket

def check_ollama_connection():
    """
    Check if Ollama server is running and accessible.
    Returns True if connection successful, False otherwise.
    """
    try:
        # Try to connect to Ollama's default port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 11434))
        sock.close()
        
        if result == 0:
            print("Ollama server is running")
            return True
        else:
            print("ERROR: Ollama server is not running. Please start it with 'ollama serve'")
            return False
    except Exception as e:
        print(f"Error checking Ollama connection: {str(e)}")
        return False

def check_image_exists(image_path):
    """
    Verify that the image file exists and is readable.
    """
    if not os.path.exists(image_path):
        print(f"ERROR: Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            # Try to read a byte to verify file is accessible
            f.read(1)
        print(f"Image file is accessible: {image_path}")
        return True
    except Exception as e:
        print(f"ERROR: Cannot read image file: {str(e)}")
        return False

def analyze_image(image_path, prompt="What is in this image?"):
    """
    Analyzes an image using Ollama's vision model with preliminary checks.
    """
    # First, perform our checks
    if not check_ollama_connection():
        raise ConnectionError("Cannot proceed without Ollama server running")
    
    if not check_image_exists(image_path):
        raise FileNotFoundError(f"Cannot proceed with invalid image: {image_path}")
    
    try:
        # Read the image file
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print("Sending image to Ollama for analysis...")
        # Send to Ollama
        response = ollama.chat(
            model='llama3.2-vision:latest',  # Make sure this matches your installed model
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_data]
            }]
        )
        
        return response
    except Exception as e:
        print(f"Error during image analysis: {str(e)}")
        raise

if __name__ == "__main__":
    image_path = "images/test.jpg"
    
    try:
        print("Starting image analysis process...")
        response = analyze_image(image_path)
        print("\nAnalysis complete!")
        print("Response:", response)
    except Exception as e:
        print(f"\nFailed to complete analysis: {str(e)}")
        print("\nPlease ensure:")
        print("1. Ollama is installed and running ('ollama serve')")
        print("2. You have a vision-capable model pulled ('ollama pull llama2-vision')")
        print("3. The image file exists and is readable")