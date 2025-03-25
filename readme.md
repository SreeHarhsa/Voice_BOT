# AI Voice Interview Assistant

## Project Overview
An interactive Streamlit application that provides a personalized AI interview experience with text and voice responses.

### Features
- Interactive interview question selection
- Text response generation
- Text-to-speech audio output
- Personal AI assistant interface

## Prerequisites
- Python 3.8+
- Google Cloud Account
- Gemini API Access

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/SreeHarhsa/Voice_BOT.git
cd Voice_BOT
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. API Key Setup
1. Obtain Google Gemini API key
2. Create a Google Cloud service account
3. Place keys in separate .docx files:
   - Gemini key: `keys/Gemini-API.docx`
   - GCP key: `keys/verbal-trainer-key.json`

### 5. Run the Application
```bash
streamlit run main.py
```

## Configuration
- Modify file paths in `main.py` for key locations
- Customize interview questions in the source code

## Troubleshooting
- Ensure all dependencies are installed
- Check API key permissions
- Verify Google Cloud credentials

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Specify your license here]

## Contact
Sai Venkata Sri Harsha Donga
Email: [Your Email]
Phone: +91 9492159509
