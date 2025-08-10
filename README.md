# AI Image Generation Pipeline

This project is an automated pipeline for generating AI images. It uses Google Gemini to create unique, descriptive prompts and then uses Google's ImageFX service to generate images based on those prompts.

## Features

- **Creative Prompt Generation**: Leverages the Google Gemini API to generate creative and detailed prompts for image generation.
- **Automated Image Generation**: Uses a Node.js-based CLI tool to interact with Google's ImageFX service and generate images.
- **Persistent Job Queue**: Utilizes a simple JSON-based database (`tinydb`) to manage a queue of prompts, ensuring that each prompt is processed.
- **Extensible**: The modular design allows for easy extension or replacement of the prompt generation and image generation components.

## How it Works

The pipeline operates in two main phases:

1.  **Prompt Population**: The `populate_prompts()` function in `src/main.py` calls the Gemini API to generate a set of new, creative prompts. These prompts are inspired by a list of examples located in `prompts_banco_imagens.json`. The new prompts are then stored in `prompts.json` with a `pending` status.

2.  **Image Creation**: The `process_pending_prompts()` function in `src/main.py` retrieves the `pending` prompts from the database. For each prompt, it calls the `imageFX-api` CLI tool, which in turn communicates with Google's ImageFX service to generate the image. Once an image is successfully generated, the corresponding prompt is marked as `completed`.

## Project Structure

```
ai-img-gen/
├── .gitignore
├── GUI_Fooocus_API.md
├── imageFX-api/
│   ├── src/
│   │   ├── cli.ts         # CLI entry point for the ImageFX API tool
│   │   ├── index.ts       # Core logic for the ImageFX API tool
│   │   └── utils/
│   │       ├── filemanager.ts # Handles file operations
│   │       └── request.ts     # Handles HTTP requests to ImageFX
│   ├── package.json
│   └── tsconfig.json
├── src/
│   ├── database_handler.py # Manages the prompt database (prompts.json)
│   ├── gemini_handler.py   # Handles interaction with the Gemini API
│   ├── imagefx_handler.py  # Python wrapper for the imageFX-api CLI
│   └── main.py             # Main script to run the pipeline
├── prompts_banco_imagens.json # Example prompts for Gemini
├── prompts.json             # Database of generated prompts
├── prompt_usage_state.json  # Tracks used example prompts
├── README.md
└── requirements.txt
```

## Technologies Used

- **Backend**: Python 3
- **Frontend/CLI**: Node.js, TypeScript
- **APIs**: Google Gemini, Google ImageFX
- **Database**: TinyDB (JSON-based)

### Python Dependencies:
- `google-generativeai`
- `python-dotenv`
- `tinydb`

### Node.js Dependencies:
- `axios`
- `cheerio`
- `yargs`

## Setup and Installation

### Prerequisites

- Python 3.7+
- Node.js 14.x+
- A Google Cloud project with the Gemini API enabled.
- A `__Secure-next-auth.session-token` cookie from a valid Google account session.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai-img-gen
    ```

2.  **Set up the Python environment:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the Node.js environment:**
    ```bash
    cd imageFX-api
    npm install
    npm run build
    cd ..
    ```

4.  **Configure environment variables:**

    Create a `.env` file in the root of the project and add the following variables:

    ```
    GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    GOOGLE_CLOUD_LOCATION="your-gcp-location"
    GOOGLE_LABS_COOKIE="__Secure-next-auth.session-token=YOUR_COOKIE_HERE"
    ```
    - Replace `"your-gcp-project-id"` and `"your-gcp-location"` with your Google Cloud project ID and location.
    - To get the `GOOGLE_LABS_COOKIE` value:
        1. Open your web browser and go to the ImageFX website.
        2. Open the developer tools (usually by pressing F12).
        3. Go to the "Application" (or "Storage") tab.
        4. Find the cookies for the `imagefx.withgoogle.com` domain.
        5. Copy the entire value of the `__Secure-next-auth.session-token` cookie.

## How to Use

To run the entire pipeline, simply execute the `main.py` script:

```bash
python src/main.py
```

This will:
1.  Generate a new batch of prompts using Gemini.
2.  Process the pending prompts to generate images using ImageFX.

The generated images will be saved in the `images` directory.
