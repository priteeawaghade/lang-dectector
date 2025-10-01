from flask import Flask, request, jsonify, send_from_directory  
import os
from flask_cors import CORS
from googletrans import Translator
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Fix random seed for reproducibility
DetectorFactory.seed = 0

app = Flask(__name__)
CORS(app)

# Initialize Translator
translator = Translator()

LANGUAGE_MAP = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'ca': 'Catalan',
    'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek',
    'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish',
    'fr': 'French', 'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian',
    'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'kn': 'Kannada',
    'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam',
    'mr': 'Marathi', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi',
    'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak',
    'sl': 'Slovenian', 'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish', 'sw': 'Swahili',
    'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Tagalog', 'tr': 'Turkish',
    'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)'
}

@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'home.html')

@app.route('/detect_language', methods=['POST'])
def detect_language():
    try:
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        language_code = detect(text)
        language_full = LANGUAGE_MAP.get(language_code, 'Unknown')

        return jsonify({'language': language_full})
    except LangDetectException as e:
        return jsonify({'error': f'Language detection error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '')
        target_language = data.get('target_language', 'en')

        if not text:
            return jsonify({'error': 'No text provided'}), 400
        print(f"Translating: {text} -> {target_language}")  # Debugging Log

        # Translate the text
        translated_text = translator.translate(text, dest=target_language).text
        print(f"Translation Result: {translated_text}")  # Debugging Log

        return jsonify({'translation': translated_text})
    except Exception as e:
        print("Translation Error:", str(e))  # Debugging Log
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
