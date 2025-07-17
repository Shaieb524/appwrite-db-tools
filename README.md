# Appwrite Database Tools

A modular Python toolkit for working with Appwrite databases, including connection testing and collection management.

## Project Structure

- `config.py` - Appwrite configuration loader
- `appwrite_client.py` - Appwrite client initialization and connection management
- `main.py` - Main script to test connection and display database information
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked in git)

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file is properly configured with your Appwrite credentials.

## Usage

### Test Connection

Run the main script to test your Appwrite connection:

```bash
python main.py
```

This will:
- Load your Appwrite configuration
- Test the connection to your Appwrite instance
- Display database and collection information
- Show details about your user_emails collection

## Features

- ✅ Modular design with separate configuration and client modules
- ✅ Configuration validation and error handling
- ✅ Connection testing with detailed feedback
- ✅ Collection information display
- ✅ Extensible architecture for future tools

## Configuration

The script uses the following environment variables from your `.env` file:
- `APPWRITE_ENDPOINT`
- `APPWRITE_PROJECT_ID`
- `APPWRITE_DATABASE_ID`
- `APPWRITE_USER_EMAILS_COLLECTION_ID`
- `APPWRITE_API_KEY`

The new collection will be created with the ID: `user_emails_test`
