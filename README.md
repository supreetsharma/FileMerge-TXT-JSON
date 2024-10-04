# File Processor

File Processor is a Streamlit web application that allows users to process .txt and .json files, select tags, and generate new .txt files with combined content.

## Features

- Upload multiple .txt and .json file pairs
- Select tags from JSON files
- Add custom tags
- Process files individually or in batches
- Preview processed files before download
- Download processed files as a ZIP archive

## Requirements

- Python 3.7+
- Streamlit
- Other dependencies listed in `pyproject.toml`

## Installation

1. Clone the repository or download the project files.

2. Install the required dependencies using Poetry:

   ```
   poetry install
   ```

   If you don't have Poetry installed, you can install it by following the instructions at https://python-poetry.org/docs/#installation

3. Alternatively, you can install the dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit app:

   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to `http://localhost:5000` (or the URL provided in the console output).

3. Use the app:
   - Upload .txt and .json files using the file upload buttons.
   - Select tags from the available options (based on the JSON files).
   - Add custom tags if desired.
   - Click the "Process Files" button to generate new content.
   - Preview the processed files in the expandable sections.
   - Download the processed files as a ZIP archive using the "Download Processed Files (ZIP)" button.

## Notes

- The app will automatically match .txt and .json files with the same name (excluding the file extension).
- Unmatched files will be processed individually.
- Make sure your JSON files contain valid JSON data (either a dictionary or a list of dictionaries).

## Deployment

This project is designed to be deployed on Replit. To deploy:

1. Create a new Repl on Replit and import the project files.
2. Set up the run command in the Replit configuration to: `streamlit run main.py`
3. Click the "Run" button to start the Streamlit app.

The app will be accessible through the provided Replit URL.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
