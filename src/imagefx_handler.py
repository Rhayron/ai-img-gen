
import subprocess
import os
import glob
from typing import List

# Absolute path to the imageFX-api CLI script
IMAGEFX_CLI_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imageFX-api', 'dist', 'cli.js'))

# Directory where images will be saved
IMAGE_OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))

def generate_image_with_imagefx(prompt: str, cookie: str) -> List[str]:
    """
    Generates an image using the imageFX-api CLI.

    Args:
        prompt: The text prompt for image generation.
        cookie: The __Secure-next-auth.session-token cookie.

    Returns:
        A list of paths to the generated images, or an empty list on failure.
    """
    if not os.path.exists(IMAGEFX_CLI_PATH):
        print(f"Error: imageFX-api CLI not found at {IMAGEFX_CLI_PATH}")
        print("Please run the build steps for imageFX-api first.")
        return []

    if not os.path.exists(IMAGE_OUTPUT_DIR):
        os.makedirs(IMAGE_OUTPUT_DIR)

    # Get the set of files in the output directory before generation
    files_before = set(os.listdir(IMAGE_OUTPUT_DIR))

    command = [
        "node",
        IMAGEFX_CLI_PATH,
        "--prompt",
        prompt,
        "--cookie",
        cookie,
        "--dir",
        IMAGE_OUTPUT_DIR,
        "--count",
        "1"  # Generate one image per prompt
    ]

    try:
        print(f"Running image generation for prompt: '{prompt}'")
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # Find the newly created file
        files_after = set(os.listdir(IMAGE_OUTPUT_DIR))
        new_files = files_after - files_before

        if not new_files:
            print(f"Warning: Image generation command finished, but no new file was found.")
            print("imageFX-api stdout:", process.stdout)
            print("imageFX-api stderr:", process.stderr)
            return []

        new_file_paths = [os.path.join(IMAGE_OUTPUT_DIR, f) for f in new_files]
        print(f"Successfully generated new image(s): {', '.join(new_file_paths)}")
        return new_file_paths

    except subprocess.CalledProcessError as e:
        print(f"Error calling imageFX-api CLI:")
        print(f"Exit Code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return []
    except FileNotFoundError:
        print("Error: 'node' command not found. Please ensure Node.js is installed and in your system's PATH.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
