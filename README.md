# ComfyUI Gemini Integration Node

This custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) provides an interface to interact with Google's Gemini API for image analysis and text-based conversations.

## Features

*   **Gemini Image Analysis:**
    *   Upload an image and provide a custom prompt to analyze its content using the Gemini model.
    *   Option to process images in a batch from a specified folder and save the results in text files.
*   **Gemini Chat:**
    *   Send text-based prompts to Gemini for interactive conversations.
*   **Automatic Dependency Installation:**
    *   The node will automatically install required Python libraries on its first execution.
    *   The node checks if libraries have already been installed in a previous execution to avoid unnecessary installation.
*   **Secure API Key Input:**
    *   Users can securely provide their API key directly in the node's input field.

## Installation

1.  **Clone the Repository:**

    ```bash
    cd ComfyUI/custom_nodes
    git clone <your_repository_url>
    ```

2.  **Restart ComfyUI:** Restart your ComfyUI instance to load the new custom node.

## How to Use

After installing and restarting ComfyUI, you will find the following nodes under the "Gemini" category:

### Gemini Analysis

1.  **Add the Node:** Add the "Gemini Analysis" node to your workflow.
2.  **Connect an Image:** Connect an "IMAGE" input from a previous node containing your image.
3.  **Provide API Key:** Enter your Google Gemini API key in the "api\_key" input field.
4.  **Enter Prompt:** Enter a custom text prompt for your image analysis in the "prompt" input field.
5.  **Run:** Execute the workflow to send your image and prompt to Gemini. The output will be the text response from Gemini.

### Gemini Batch Analysis

1.  **Add the Node:** Add the "Gemini Batch Analysis" node to your workflow.
2.  **Input Folder:** Enter the path to a folder containing images in the "input\_folder" field.
3.  **Provide API Key:** Enter your Google Gemini API key in the "api\_key" input field.
4.  **Enter Prompt:** Enter a custom text prompt for your image analysis in the "prompt" input field.
5.  **Run:** The node will process all image files in the specified folder. The output text will be a summary of processed files, and the Gemini response for each file will be saved in a corresponding text file.

### Gemini Chat

1.  **Add the Node:** Add the "Gemini Chat" node to your workflow.
2.  **Provide API Key:** Enter your Google Gemini API key in the "api\_key" input field.
3.  **Enter Prompt:** Enter a text prompt for your conversation in the "prompt" input field.
4.  **Run:** The output will be the text response from Gemini.

## Important Notes

*   **API Key Security:** Keep your API key secure. Do not share workflows containing your API key with untrusted sources.
*   **First Run Installation:** The first time you use the custom nodes after a ComfyUI restart, the node will attempt to automatically install the missing libraries.
*   **State File:** The first time the custom node is loaded, a `gemini_node_state.json` will be created in the same directory as the `__init__.py` file. This file is used to store the installation state.
*   **Troubleshooting:** If you encounter issues, check the console output of your ComfyUI for any error messages.

## Requirements

*   [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
*   `google-generativeai`
*   `Pillow`
*   `numpy`

These packages will be automatically installed during the first run, if they are not already installed.

## License

[Insert your desired license here]

## Contributing

Feel free to contribute by creating pull requests to add new features, fix bugs, or improve documentation.

## Contact

If you have any questions or suggestions, please open an issue in the repository.
