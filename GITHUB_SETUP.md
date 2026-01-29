# GitHub Setup Instructions

## Step 1: Create GitHub Repository for webhook-repo

1. Go to https://github.com/new
2. Fill in the following:
   - **Repository name:** `webhook-repo`
   - **Description:** GitHub webhook receiver for capturing Push, Pull Request, and Merge events
   - **Public/Private:** Public (recommended for submission)
   - **Initialize with README:** No (we already have one)
3. Click "Create repository"

## Step 2: Add Remote and Push Code

After creating the repository, you'll see instructions. Run these commands:

```bash
# Navigate to your webhook-repo directory
cd c:\Users\alank\OneDrive\Desktop\webhook-repo

# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/alan-srivastava/webhook-repo.git

# Rename branch to main (if not already)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/alan-srivastava/webhook-repo.git
git branch -M main
git push -u origin main
```

## Step 3: Configure GitHub Webhook in action-repo

1. Go to: https://github.com/alan-srivastava/action-repo
2. Click **Settings** (top navigation)
3. Click **Webhooks** (left sidebar)
4. Click **Add webhook**
5. Fill in:
   - **Payload URL:** 
     - For local testing: Use ngrok URL (see below)
     - For production: Your deployed server URL (e.g., https://webhook-repo.herokuapp.com/webhook)
   - **Content type:** Select `application/json`
   - **Which events would you like to trigger this webhook?**
     - Check: ✅ Push events
     - Check: ✅ Pull request events
     - Uncheck: Pull request review comments
   - **Active:** ✅ Checked
6. Click **Add webhook**

## Step 4: Local Testing with ngrok

To test locally without deploying:

### Download ngrok
1. Go to https://ngrok.com/download
2. Download for Windows
3. Extract to a folder (e.g., C:\ngrok)

### Run ngrok
```bash
# In a separate terminal
C:\ngrok\ngrok http 5000
```

You'll see output like:
```
ngrok                                                       (Ctrl+C to quit)

Session Status                online
Account                       <your-account>
Version                       3.x.x
Region                        us (United States)
Latency                       xx ms
Web Interface                 http://127.0.0.1:4040

Forwarding                    https://abc123def456.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     dl      ul      cl
                              0       0       0       0       0
```

Copy the HTTPS URL: `https://abc123def456.ngrok.io`

### Configure Webhook with ngrok URL
1. In action-repo settings → Webhooks
2. Payload URL: `https://abc123def456.ngrok.io/webhook`
3. Save the webhook

## Step 5: Test the Webhook

### Run Flask App (in original terminal)
```bash
cd c:\Users\alank\OneDrive\Desktop\webhook-repo
python app.py
```

### Test Push Event
```bash
cd c:\Users\alank\OneDrive\Desktop\action-repo
echo "test content" > test.txt
git add test.txt
git commit -m "Test webhook"
git push origin main
```

### Check Results
1. **GitHub:** Go to action-repo → Settings → Webhooks → [Your webhook] → Recent Deliveries
   - Should show a request with status 200
2. **Flask:** Check the console output for "Document inserted"
3. **UI:** Go to http://localhost:5000 (or ngrok URL)
   - Should show the new action

### Test Pull Request Event
1. Create a new branch in action-repo
2. Make a commit and push
3. Open a Pull Request on GitHub
4. Watch the webhook trigger

### Test Merge Event
1. Merge the PR to main
2. Watch the webhook trigger with action="MERGE"

## Step 6: Verify Everything Works

Checklist:
- ✅ Flask app running without errors
- ✅ MongoDB connected successfully
- ✅ Webhook endpoint accessible
- ✅ GitHub webhooks sending events
- ✅ Events stored in MongoDB
- ✅ UI displaying events in real-time (every 15 seconds)
- ✅ Timestamps formatted correctly
- ✅ Author information captured
- ✅ Branch names displayed correctly

## Troubleshooting

### Webhook not delivering
- Check webhook URL is correct and accessible
- Verify Flask app is running
- Check firewall/antivirus settings
- Use ngrok for local testing

### Events not appearing in UI
- Refresh the page
- Check MongoDB connection
- Verify event type is PUSH, PULL_REQUEST, or MERGE
- Check Flask console logs

### MongoDB connection error
- Verify MONGO_URI in .env file
- Add your IP to MongoDB Atlas whitelist:
  1. Go to MongoDB Atlas → Network Access
  2. Click "Add IP Address"
  3. Add current IP or use 0.0.0.0/0

## Final Submission

When ready to submit:

1. **Repository URLs to provide:**
   - action-repo: https://github.com/alan-srivastava/action-repo.git
   - webhook-repo: https://github.com/alan-srivastava/webhook-repo.git

2. **Verify before submission:**
   - Both repositories exist on GitHub
   - webhook-repo code is pushed
   - action-repo has webhook configured
   - UI is working and polling MongoDB
   - At least one webhook event has been received and stored

3. **What the evaluator will do:**
   - Clone webhook-repo
   - Install dependencies
   - Run the Flask app
   - Configure webhook in action-repo (or test with provided events)
   - Verify UI displays events correctly
   - Check MongoDB for stored data

## Sample Webhook Event Data

When everything is working, your MongoDB should have documents like:

```json
{
  "_id": ObjectId("..."),
  "request_id": "a1b2c3d",
  "author": "alan-srivastava",
  "action": "PUSH",
  "from_branch": "main",
  "to_branch": "main",
  "timestamp": "2024-01-29T10:30:45.123Z"
}
```

And your UI should display:
```
"alan-srivastava" pushed to "main" on Jan 29, 2024 - 10:30 AM UTC
```

---

**You're all set! Good luck with the submission! 🚀**
