# US Presidential Election 2024 Sentiment Analysis Tool

## Description
This project analyzes the comments from the top 10 YouTube search videos about the US 2024 Presidential Election to determine its sentiment (positive, negative, or neutral).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/zaramerchant/us24-election-sentiment-analysis.git
   cd us24-election-sentiment-analysis
   ```

2. Setting up a virtual environment (reccomended):
    Write this in your terminal: 
    ```bash 
    python -m venv venv
    ```
    Activate the virtual environment with the following command:
    ```bash
    source ./venv/bin/activate
    ```

3. Setting Up the API Key

This project requires an API key to access the YouTube Data API. Follow these steps to create a `config.py` file and store your API key securely:

    1. **Get an API Key**:
        - Go to Google Cloud Console: https://console.cloud.google.com/
        - Enable the YouTube Data API
        - Generate an API key and copy it
    2. **Create a `config.py` File**:
        Create a file named `config.py` in the same place as `main.py`. 
        ```bash
        touch config.py
        ```
    3. **Put the API Key in the file**
        ```bash
        API_KEY = "YOUR_API_KEY"
        ```

4. Install Dependencies
    Install the required Python packages using pip:
    ```bash
    pip install pandas google-api-python-client textblob plotly nltk
    ```