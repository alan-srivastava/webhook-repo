from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://Python:Alankrit@cluster0.nzavehg.mongodb.net/')
DB_NAME = 'github_webhooks'
COLLECTION_NAME = 'actions'

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

@app.route('/')
def index():
    """Serve the UI"""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive GitHub webhook"""
    try:
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No payload received'}), 400
        
        # Determine action type
        action = None
        author = None
        from_branch = None
        to_branch = None
        request_id = None
        timestamp = None
        
        # Handle PUSH event
        if 'push' in request.headers.get('X-GitHub-Event', ''):
            action = 'PUSH'
            author = payload.get('pusher', {}).get('name', 'Unknown')
            to_branch = payload.get('ref', '').split('/')[-1]
            from_branch = to_branch
            request_id = payload.get('head_commit', {}).get('id', '')[:7] if payload.get('head_commit') else ''
            timestamp = payload.get('head_commit', {}).get('timestamp', datetime.utcnow().isoformat()) if payload.get('head_commit') else datetime.utcnow().isoformat()
        
        # Handle PULL_REQUEST event
        elif 'pull_request' in request.headers.get('X-GitHub-Event', ''):
            action = 'PULL_REQUEST'
            author = payload.get('pull_request', {}).get('user', {}).get('login', 'Unknown')
            from_branch = payload.get('pull_request', {}).get('head', {}).get('ref', '')
            to_branch = payload.get('pull_request', {}).get('base', {}).get('ref', '')
            request_id = str(payload.get('pull_request', {}).get('id', ''))
            timestamp = payload.get('pull_request', {}).get('created_at', datetime.utcnow().isoformat())
        
        # Handle MERGE event (through push to main/master or pull_request merged)
        elif 'pull_request' in request.headers.get('X-GitHub-Event', '') and payload.get('pull_request', {}).get('merged'):
            action = 'MERGE'
            author = payload.get('pull_request', {}).get('merged_by', {}).get('login', 'Unknown')
            from_branch = payload.get('pull_request', {}).get('head', {}).get('ref', '')
            to_branch = payload.get('pull_request', {}).get('base', {}).get('ref', '')
            request_id = str(payload.get('pull_request', {}).get('id', ''))
            timestamp = payload.get('pull_request', {}).get('merged_at', datetime.utcnow().isoformat())
        else:
            return jsonify({'error': 'Unsupported event type'}), 400
        
        # Validate required fields
        if not all([action, author, to_branch]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create document
        document = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch or to_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
        
        # Insert into MongoDB
        result = collection.insert_one(document)
        
        print(f"Document inserted: {result.inserted_id}")
        return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 201
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/actions', methods=['GET'])
def get_actions():
    """Get all actions from MongoDB"""
    try:
        actions = list(collection.find({}).sort('timestamp', -1).limit(50))
        
        # Convert ObjectId to string for JSON serialization
        for action in actions:
            action['_id'] = str(action['_id'])
        
        return jsonify(actions), 200
    except Exception as e:
        print(f"Error fetching actions: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
