# Setup and Testing Guide for Webhook Repository

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- MongoDB Atlas account (already provided)

### Step 1: Clone and Install
```bash
# Clone the repository
git clone https://github.com/alan-srivastava/webhook-repo.git
cd webhook-repo

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 3: Access the UI
Open your browser and visit: `http://localhost:5000`

## Testing with Webhooks

### Local Testing with ngrok

If testing locally, you need to expose your local server to the internet using ngrok:

1. Download ngrok from https://ngrok.com/download
2. Run ngrok: `ngrok http 5000`
3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. Use this URL in your GitHub webhook configuration

### Configure GitHub Webhook in action-repo

1. Go to your action-repo: https://github.com/alan-srivastava/action-repo
2. Navigate to **Settings → Webhooks**
3. Click **Add webhook**
4. Fill in the following:
   - **Payload URL**: `https://your-webhook-domain.com/webhook` (or ngrok URL for local testing)
   - **Content type**: `application/json`
   - **Which events would you like to trigger this webhook?**: Select the following:
     - ✓ Push events
     - ✓ Pull requests
     - ✓ Workflow runs (optional)
   - **Active**: ✓ Check the box
5. Click **Add webhook**

### Testing Webhook Events

#### Test 1: Test Webhook Delivery
1. After adding the webhook, GitHub shows a green checkmark and "Recent Deliveries"
2. Scroll down to the webhook and click on the most recent delivery
3. You should see details and a response status

#### Test 2: Trigger a PUSH event
```bash
cd action-repo
# Make a change and commit
echo "test content" > test.txt
git add test.txt
git commit -m "Test push event"
git push origin main
```

The webhook should trigger automatically. Check:
- GitHub webhook Recent Deliveries tab (should show 200 status)
- Flask console logs
- MongoDB Atlas dashboard under `github_webhooks` database, `actions` collection

#### Test 3: Trigger a PULL_REQUEST event
1. Create a new branch in action-repo
2. Make a change and push the branch
3. Create a Pull Request on GitHub
4. The webhook should trigger automatically

#### Test 4: Trigger a MERGE event
1. After creating a PR, merge it to main/master branch
2. The webhook should trigger when the PR is merged

## Monitoring and Debugging

### Check Flask Logs
```
Connected to MongoDB successfully
* Running on http://0.0.0.0:5000
* Document inserted: <ObjectID>
```

### Check Webhook in GitHub
1. Go to action-repo → Settings → Webhooks
2. Click on the webhook
3. Scroll down to "Recent Deliveries"
4. Click on each delivery to see request/response details
5. Check the response status code (200 is success)

### Check MongoDB Data
1. Visit MongoDB Atlas: https://account.mongodb.com/account/login
2. Go to Collections in the `github_webhooks` database
3. Click on the `actions` collection to view stored documents

## API Endpoints

### GET /
Returns the UI dashboard

### POST /webhook
Receives GitHub webhook events

**Expected Headers:**
- `X-GitHub-Event`: push, pull_request

**Request Body:** GitHub webhook payload

**Response:**
- Success: `{"status": "success", "id": "mongoid"}`
- Error: `{"error": "error message"}`

### GET /api/actions
Returns all stored actions from MongoDB (50 most recent)

**Response:** Array of action objects
```json
[
  {
    "_id": "...",
    "request_id": "abc123",
    "author": "username",
    "action": "PUSH",
    "from_branch": "main",
    "to_branch": "main",
    "timestamp": "2024-01-29T10:30:00Z"
  }
]
```

## Troubleshooting

### MongoDB Connection Error
**Error:** `Cannot connect to MongoDB`
**Solution:** 
- Verify MongoDB URI in `.env` file
- Add your current IP to MongoDB Atlas whitelist:
  1. Go to MongoDB Atlas → Network Access
  2. Click "Add IP Address"
  3. Select "Add Current IP Address" or use 0.0.0.0/0 for testing (not recommended for production)

### Webhook Not Receiving Events
**Error:** No events appearing in the database
**Solution:**
- Check if webhook is active in GitHub settings (green checkmark)
- Verify the Payload URL is correct and accessible
- Check GitHub webhook Recent Deliveries tab for errors
- Check Flask console for error messages

### Flask App Won't Start
**Error:** `AttributeError: module 'pkgutil' has no attribute 'get_loader'`
**Solution:**
```bash
pip install --upgrade Flask
pip install -r requirements.txt
```

### Port Already in Use
**Error:** `Address already in use`
**Solution:**
```bash
# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -i :5000
kill -9 <PID>
```

## File Structure
```
webhook-repo/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore rules
├── Procfile             # Deployment configuration
├── README.md            # Project documentation
├── SETUP.md            # This file
├── templates/
│   └── index.html       # UI dashboard
└── venv/                # Virtual environment
```

## Next Steps

1. ✅ Webhook receiver is running
2. ✅ MongoDB connection is established
3. ✅ UI is accessible at localhost:5000
4. 📝 Configure GitHub webhook to point to your server
5. 🔄 Test webhook events by pushing/creating PRs in action-repo
6. 📊 Monitor data in MongoDB and UI

## Deployment

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

Or deploy to services like:
- Heroku
- Railway
- Render
- AWS EC2
- Azure App Service
- Google Cloud Run

## Support

For issues or questions, check:
- Flask documentation: https://flask.palletsprojects.com/
- PyMongo documentation: https://pymongo.readthedocs.io/
- GitHub Webhooks: https://docs.github.com/en/developers/webhooks-and-events/webhooks
