import os
import base64
import subprocess
import sys
import json

# Determine the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants for state management
STATE_FILE = os.path.join(SCRIPT_DIR, "gemini_node_state.json")


# Function to load the state
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"packages_installed": False}  # Handle errors gracefully
    else:
        return {"packages_installed": False}

# Function to save the state
def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving state: {e}")

# Load the initial state
_state = load_state()
_packages_installed = _state.get("packages_installed", False)

# Function to check if a package is installed
def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

# Function to install a package using pip
def install_package(package_name):
    try:
        print(f"Installing {package_name}...")
        command = [sys.executable, "-m", "pip", "install", package_name]
        print(f"Executing command: {' '.join(command)}")
        subprocess.check_call(
            command,
        )
        print(f"{package_name} installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
       print(f"Error installing {package_name}: {e}")
       return False

# List of required packages
REQUIRED_PACKAGES = ["google-generativeai", "Pillow", "numpy"]

# Check and install packages if not already installed
if not _packages_installed:
    for package_name in REQUIRED_PACKAGES:
        if not is_package_installed(package_name):
            if not install_package(package_name):
                print(f"Failed to install {package_name}. Please install it manually.")
    _state["packages_installed"] = True # set the installation flag to true
    _packages_installed = True # set the local variable to true
    save_state(_state) # save the state to the json

import google.generativeai as genai
from PIL import Image
from io import BytesIO
import folder_paths
import numpy as np


# ComfyUI Nodes
class GeminiAnalysisNode:
    """
    Node to analyze images using Gemini
    """
    FUNCTION = "process"
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        """
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),  # API Key input
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "give a detailed caption of the image.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    CATEGORY = "Gemini"

    def process(self, image, api_key, prompt):
        """
        Analyzes a single image using the Gemini API.
        """
        if not api_key:
            return ("Error: Please provide an API key.",)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

        if image is None:
           return "Please input an image.",

        try:
            # Convert the ComfyUI image tensor to PIL image
            i = 255.0 * image.cpu().numpy()
            i = np.clip(i, 0, 255).astype(np.uint8)

            # Handle both batched and non-batched images correctly
            if i.ndim == 4:
                i = i.squeeze(0) if i.shape[0] == 1 else i  # remove batch dimension if present
            if i.ndim == 3 and i.shape[0] < i.shape[2]:
                i = i.transpose(1, 2, 0)  # Reorder to HWC
            elif i.ndim == 2:
               #convert grayscale image to 3 channels
               i=np.stack((i,i,i),axis=-1)

            img = Image.fromarray(i)

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            image_bytes = buffered.getvalue()

            prompt = f"{prompt} \n Image:"
            response = model.generate_content([{'mime_type': 'image/png', 'data': image_bytes}, prompt])
            return (response.text,)
        except Exception as e:
            return (f"An error occurred: {e}",)

class GeminiBatchAnalysisNode:
    """
    Node to analyze multiple images from a folder using Gemini
    """
    FUNCTION = "process"
    def __init__(self):
       pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        """
        return {
            "required": {
                "input_folder": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": ("STRING", {"default": ""}),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "give a detailed caption of the image.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    CATEGORY = "Gemini"

    def process(self, input_folder, api_key, prompt):
        """
        Analyzes multiple images from a folder and saves the results.
        """
        if not api_key:
             return ("Error: Please provide an API key.",)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

        if not os.path.exists(input_folder):
           return (f"Input folder not found: {input_folder}",)

        results = []
        for filename in os.listdir(input_folder):
            filepath = os.path.join(input_folder, filename)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                    with Image.open(filepath) as img:
                        # Convert the image to bytes
                        buffered = BytesIO()
                        img.save(buffered, format="PNG")
                        image_bytes = buffered.getvalue()

                        prompt = f"{prompt} \n Image:"
                        response = model.generate_content([{'mime_type': 'image/png', 'data': image_bytes}, prompt])

                        # Save the response as .txt file
                        txt_filepath = os.path.splitext(filepath)[0] + ".txt"
                        with open(txt_filepath, "w", encoding="utf-8") as txt_file:
                            txt_file.write(response.text)

                        results.append(f"Processed: {filename} -> {txt_filepath}")
                except Exception as e:
                   results.append(f"Error processing {filename}: {e}")

        return ("\n".join(results),)

class GeminiChatNode:
    """
    Node to have a text-based conversation with Gemini
    """
    FUNCTION = "process"
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        """
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "Hello, how can I help you?",
                    },
                ),
                "api_key": ("STRING", {"default": ""}), # API key input
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    CATEGORY = "Gemini"

    def process(self, prompt, api_key):
        """
        Sends a text prompt to Gemini and returns the response.
        """
        if not api_key:
            return ("Error: Please provide an API key.",)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

        try:
            response = model.generate_content(prompt)
            return (response.text,)
        except Exception as e:
            return (f"An error occurred: {e}",)


# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "GeminiAnalysis": GeminiAnalysisNode,
    "GeminiBatchAnalysis": GeminiBatchAnalysisNode,
    "GeminiChat": GeminiChatNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAnalysisNode": "Gemini Analysis",
    "GeminiBatchAnalysisNode": "Gemini Batch Analysis",
    "GeminiChatNode": "Gemini Chat"
}
