# LexiCode Plagiarism Detector

A fully offline web application for plagiarism detection built with Flask, scikit-learn, and NLTK.

## Setup and Run

1. Clone or download this repository.
2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the NLTK setup script to download required data:
   ```bash
   python setup_nltk.py
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open your browser and navigate to `http://127.0.0.1:5000`.

## Demo Account
Email: demo@lexicode.com
Password: Demo@1234
