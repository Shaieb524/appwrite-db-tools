from config import config
from appwrite_client import appwrite_client
from appwrite.exception import AppwriteException
import time

def duplicate_collection():
    print("Getting source collection details...")
    
    source_collection = appwrite_client.get_collection_info(config.user_emails_collection_id)
    if not source_collection:
        print("Failed to get source collection")
        return False
    
    print(f"Found source collection: {source_collection['name']}")
    
    existing_collection = appwrite_client.get_collection_info(config.new_collection_id)
    if existing_collection:
        print(f"Collection '{config.new_collection_id}' already exists")
        return False
    
    print(f"Creating new collection '{config.new_collection_id}'...")
    
    try:
        new_collection = appwrite_client.databases.create_collection(
            database_id=config.database_id,
            collection_id=config.new_collection_id,
            name=config.new_collection_name,
            permissions=source_collection.get('permissions', []),
            document_security=source_collection.get('documentSecurity', False),
            enabled=source_collection.get('enabled', True)
        )
        print(f"Created collection: {new_collection['name']}")
    except AppwriteException as e:
        print(f"Failed to create collection: {e.message}")
        return False
    
    print("Copying attributes...")
    for attr in source_collection['attributes']:
        attr_type = attr['type']
        attr_key = attr['key']
        
        try:
            if attr_type == 'string':
                appwrite_client.databases.create_string_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    size=attr['size'],
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False),
                    encrypt=attr.get('encrypt', False)
                )
            elif attr_type == 'integer':
                appwrite_client.databases.create_integer_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    min=attr.get('min'),
                    max=attr.get('max'),
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'float':
                appwrite_client.databases.create_float_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    min=attr.get('min'),
                    max=attr.get('max'),
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'boolean':
                appwrite_client.databases.create_boolean_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'datetime':
                appwrite_client.databases.create_datetime_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'email':
                appwrite_client.databases.create_email_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'url':
                appwrite_client.databases.create_url_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'enum':
                appwrite_client.databases.create_enum_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    elements=attr['elements'],
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'ip':
                appwrite_client.databases.create_ip_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    key=attr_key,
                    required=attr['required'],
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            elif attr_type == 'relationship':
                appwrite_client.databases.create_relationship_attribute(
                    database_id=config.database_id,
                    collection_id=config.new_collection_id,
                    related_collection_id=attr['relatedCollection'],
                    type=attr['relationType'],
                    two_way=attr.get('twoWay', False),
                    key=attr_key,
                    two_way_key=attr.get('twoWayKey'),
                    on_delete=attr.get('onDelete', 'restrict')
                )
            
            print(f"  Added attribute: {attr_key} ({attr_type})")
            
        except AppwriteException as e:
            print(f"  Failed to add attribute {attr_key}: {e.message}")
    
    print("Waiting for attributes to be ready...")
    time.sleep(3)
    
    print("Copying indexes...")
    for index in source_collection.get('indexes', []):
        try:
            appwrite_client.databases.create_index(
                database_id=config.database_id,
                collection_id=config.new_collection_id,
                key=index['key'],
                type=index['type'],
                attributes=index['attributes'],
                orders=index.get('orders', [])
            )
            print(f"  Added index: {index['key']}")
        except AppwriteException as e:
            print(f"  Failed to add index {index['key']}: {e.message}")
    
    print("Copying documents...")
    offset = 0
    limit = 25
    total_copied = 0
    
    while True:
        try:
            documents = appwrite_client.databases.list_documents(
                database_id=config.database_id,
                collection_id=config.user_emails_collection_id,
                queries=[f"limit({limit})", f"offset({offset})"]
            )
            
            if not documents['documents']:
                break
            
            for doc in documents['documents']:
                doc_data = {k: v for k, v in doc.items() if not k.startswith('$')}
                
                try:
                    appwrite_client.databases.create_document(
                        database_id=config.database_id,
                        collection_id=config.new_collection_id,
                        document_id=doc['$id'],
                        data=doc_data,
                        permissions=doc.get('$permissions', [])
                    )
                    total_copied += 1
                    print(f"  Copied document {total_copied}: {doc['$id']}")
                except AppwriteException as e:
                    print(f"  Failed to copy document {doc['$id']}: {e.message}")
            
            offset += limit
            
            if len(documents['documents']) < limit:
                break
                
        except AppwriteException as e:
            print(f"Failed to get documents: {e.message}")
            break
    
    print(f"Collection duplicated successfully")
    print(f"Total documents copied: {total_copied}")
    print(f"New collection ID: {config.new_collection_id}")
    return True

def main():
    print("Testing connection...")
    if not appwrite_client.test_connection():
        print("Connection failed")
        return
    
    print("Connection successful")
    if duplicate_collection():
        print("Duplication completed")
    else:
        print("Duplication failed")

if __name__ == "__main__":
    main()
