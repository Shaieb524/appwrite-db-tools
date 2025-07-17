from config import config
from appwrite_client import appwrite_client
from appwrite.exception import AppwriteException

def empty_collection():
    if not config.collection_to_be_emptied_id:
        print("Error: APPWRITE_COLLECTION_TOBE_EMPTIES_ID not set in .env file")
        return False
    
    print("Getting collection details...")
    
    collection_info = appwrite_client.get_collection_info(config.collection_to_be_emptied_id)
    if not collection_info:
        print("Failed to get collection info")
        return False
    
    print(f"Found collection: {collection_info['name']}")
    print(f"Collection ID: {config.collection_to_be_emptied_id}")
    
    print("Fetching documents to delete...")
    total_deleted = 0
    
    while True:
        try:
            documents = appwrite_client.databases.list_documents(
                database_id=config.database_id,
                collection_id=config.collection_to_be_emptied_id,
                queries=["limit(25)"]
            )
            
            if not documents['documents']:
                break
            
            for doc in documents['documents']:
                try:
                    appwrite_client.databases.delete_document(
                        database_id=config.database_id,
                        collection_id=config.collection_to_be_emptied_id,
                        document_id=doc['$id']
                    )
                    total_deleted += 1
                    print(f"  Deleted document {total_deleted}: {doc['$id']}")
                except AppwriteException as e:
                    print(f"  Failed to delete document {doc['$id']}: {e.message}")
            
            if len(documents['documents']) < 25:
                break
                
        except AppwriteException as e:
            print(f"Failed to get documents: {e.message}")
            break
    
    print(f"Collection emptied successfully")
    print(f"Total documents deleted: {total_deleted}")
    return True

def main():
    print("Testing connection...")
    if not appwrite_client.test_connection():
        print("Connection failed")
        return
    
    print("Connection successful")
    if empty_collection():
        print("Collection emptied successfully")
    else:
        print("Failed to empty collection")

if __name__ == "__main__":
    main()
