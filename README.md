# Mail Sorter

## Prerequisites

- Python 3.x installed
- Gmail API activated in Google Cloud Console
- Ollama installed with Mistral model

## Installation

1. clone this repository:
   ```bash
   git clone https://github.com/ulvy11/mail_sorter.git
   cd mail_sorter
   ```
2. Install Python dependencies :
   ```bash
   pip install -r requirements.txt
   ```
3. Add configuration files :
   - Configure `credentials.json` file for Gmail API.

## Usage

Launch main script :

```bash
python3 main.py
```

You will be asked to choose between 4 choices:

1. Generate labels for mails in your inbox without user label
2. Check for generated labels and transform them
3. Set generated then transformed labels, and removing `inbox` label
4. Delete mails with category promotion without user label
