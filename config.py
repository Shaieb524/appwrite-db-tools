import os
from dotenv import load_dotenv

load_dotenv()

class AppwriteConfig:
    def __init__(self):
        self.endpoint = os.getenv('APPWRITE_ENDPOINT')
        self.project_id = os.getenv('APPWRITE_PROJECT_ID')
        self.database_id = os.getenv('APPWRITE_DATABASE_ID')
        self.user_emails_collection_id = os.getenv('APPWRITE_USER_EMAILS_COLLECTION_ID')
        self.api_key = os.getenv('APPWRITE_API_KEY')
        self._validate_config()
    
    def _validate_config(self):
        required_fields = {
            'endpoint': self.endpoint,
            'project_id': self.project_id,
            'database_id': self.database_id,
            'user_emails_collection_id': self.user_emails_collection_id,
            'api_key': self.api_key
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")

config = AppwriteConfig()
