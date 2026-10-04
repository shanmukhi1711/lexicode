import os
import ssl
import nltk

def setup_nltk():
    print("Downloading NLTK data...")
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
        
    nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
    if not os.path.exists(nltk_data_dir):
        os.makedirs(nltk_data_dir)
    nltk.data.path.append(nltk_data_dir)
    
    try:
        nltk.download("punkt", download_dir=nltk_data_dir, quiet=True)
        nltk.download("punkt_tab", download_dir=nltk_data_dir, quiet=True)
        nltk.download("stopwords", download_dir=nltk_data_dir, quiet=True)
        print("NLTK data downloaded successfully.")
    except Exception as e:
        print(f"Failed to download NLTK data: {e}")
        print("Offline fallback will be used.")

if __name__ == "__main__":
    setup_nltk()
