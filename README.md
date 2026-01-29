# Webhook Repository - GitHub Actions Receiver

This is a Flask-based webhook receiver that captures GitHub repository events (Push, Pull Request, Merge) and stores them in MongoDB.

## Architecture

- **Webhook Receiver**: Flask application that receives GitHub webhooks
- **Database**: MongoDB for storing webhook data
- **Frontend**: Real-time UI that polls MongoDB every 15 seconds to display latest actions

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/alan-srivastava/webhook-repo.git
cd webhook-repo
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Update `.env` file with your MongoDB URI (already configured):
```
MONGO_URI=mongodb+srv://Python:Alankrit@cluster0.nzavehg.mongodb.net/
```

### 5. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## MongoDB Schema

```javascript
{
  _id: ObjectID,
  request_id: string,           // Git commit hash or PR ID
  author: string,               // GitHub username
  action: string,               // "PUSH", "PULL_REQUEST", or "MERGE"
  from_branch: string,          // Source branch
  to_branch: string,            // Target branch
  timestamp: string             // ISO UTC datetime
}
```

## Supported Events

### PUSH
- **Format**: `{author} pushed to {to_branch} on {timestamp}`
- **Example**: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC

### PULL_REQUEST
- **Format**: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **Example**: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC

### MERGE
- **Format**: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`
- **Example**: "Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC

## GitHub Webhook Configuration

### In action-repo:

1. Go to Settings → Webhooks → Add webhook
2. Set **Payload URL** to: `http://<your-domain>/webhook` (or use ngrok for local testing)
3. Set **Content type** to: `application/json`
4. Select events:
   - Push events
   - Pull request events
5. Click "Add webhook"

## API Endpoints

### POST /webhook
Receives GitHub webhook events
- **Headers**: `X-GitHub-Event` (push, pull_request)
- **Body**: GitHub webhook payload

### GET /api/actions
Returns all stored actions from MongoDB (sorted by most recent)
- **Response**: Array of action objects

### GET /
Serves the real-time UI dashboard

## Features

- ✅ Real-time webhook receiving
- ✅ MongoDB integration for persistent storage
- ✅ Automatic polling UI (every 15 seconds)
- ✅ Clean, minimal design
- ✅ Support for PUSH, PULL_REQUEST, and MERGE events
- ✅ Responsive design for mobile devices

## Notes

- The UI automatically polls MongoDB every 15 seconds for new actions
- Data is displayed with only essential information
- Timestamps are converted to user's local timezone in the UI
- The dashboard shows the 50 most recent actions

## Troubleshooting

### MongoDB Connection Error
- Verify MongoDB URI in `.env` file
- Ensure you have network access to MongoDB Atlas (whitelist your IP)

### Webhook Not Receiving Events
- Verify the webhook URL in GitHub settings
- Check Flask application logs for errors
- Use ngrok to expose local server: `ngrok http 5000`

## Related Repository
- **action-repo**: https://github.com/alan-srivastava/action-repo.git

## License
MIT
