# Mail Sorter

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/) installed (x $\geq$ 12)
- Gmail API activated in Google Cloud Console
  - [Doc to create credentials](https://developers.google.com/identity/protocols/oauth2/web-server?hl=fr#creatingcred)
- [Ollama](https://ollama.com/download) installed

## Pull Mistral model

```bash
ollama pull mistral
```

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
python main.py
```

You will be asked to choose between 4 choices:

1. Generate labels for mails in your inbox without user label
2. Check for generated labels and transform them
3. Set generated then transformed labels, and removing `inbox` label
4. Do all three
