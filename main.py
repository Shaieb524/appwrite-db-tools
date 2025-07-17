from config import config
from appwrite_client import appwrite_client

def main():
    print("Testing Appwrite connection...")
    
    connection_successful = appwrite_client.test_connection()
    
    if connection_successful:
        collections = appwrite_client.list_collections()
        if collections:
            print(f"Found {len(collections['collections'])} collections")
            for collection in collections['collections']:
                print(f"  {collection['name']} (ID: {collection['$id']})")
        
        collection_info = appwrite_client.get_collection_info(config.user_emails_collection_id)
        if collection_info:
            print(f"User emails collection: {collection_info['name']}")
            print(f"  Attributes: {len(collection_info['attributes'])}")
            print(f"  Indexes: {len(collection_info.get('indexes', []))}")
            
            if collection_info['attributes']:
                print("Attributes:")
                for attr in collection_info['attributes']:
                    print(f"  {attr['key']} ({attr['type']}) - Required: {attr['required']}")
        
        print("Connection test successful")
    else:
        print("Connection test failed")

if __name__ == "__main__":
    main()
