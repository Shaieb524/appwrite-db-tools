from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from config import config

class AppwriteClient:
    def __init__(self):
        self.client = None
        self.databases = None
        self._initialize_client()
    
    def _initialize_client(self):
        self.client = Client()
        self.client.set_endpoint(config.endpoint)
        self.client.set_project(config.project_id)
        self.client.set_key(config.api_key)
        self.databases = Databases(self.client)
    
    def test_connection(self):
        try:
            databases_list = self.databases.list()
            database = self.databases.get(config.database_id)
            return True
        except AppwriteException:
            return False
        except Exception:
            return False
    
    def get_collection_info(self, collection_id):
        try:
            collection = self.databases.get_collection(
                database_id=config.database_id,
                collection_id=collection_id
            )
            return collection
        except AppwriteException:
            return None
    
    def list_collections(self):
        try:
            collections = self.databases.list_collections(
                database_id=config.database_id
            )
            return collections
        except AppwriteException:
            return None

appwrite_client = AppwriteClient()
