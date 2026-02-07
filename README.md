# Bobthebot - Tenant Maintenance AI Agent - MVP Demo

A minimal working prototype of an AI-powered tenant maintenance request system. Tenants message a Telegram bot with maintenance issues, and the system automatically classifies, prioritizes, estimates costs, and assigns vendors.

## What This Demo Does

- Receives maintenance requests via Telegram bot
- Classifies issues (Plumbing, AC, Electrical, General)
- Assigns priority levels (LOW, MEDIUM, HIGH)
- Estimates costs in AED
- Auto-assigns vendors OR flags for human approval (>1000 AED)

## Current Status

**This is a demo MVP with mocked AI logic.** The structure and flow are production-ready, but:

- ✅ Real: Telegram bot integration
- ⚠️ Mocked: AI classification (simple keyword matching in `mock_logic.py`)
- ⚠️ Mocked: Vendor assignment (static JSON file)
- ⚠️ No database: All in-memory processing
- ⚠️ No real vendor APIs: Future integration

In production, the mock logic will be replaced with a real AI agent.

## Quick Start

### 1. Install Dependencies

```bash
# Optional but recommended: Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Get a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Choose a name (e.g., "My Tenant Bot")
4. Choose a username (e.g., "my_tenant_maintenance_bot")
5. BotFather will give you a token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### 3. Configure Environment

```bash
# Copy the example config
cp config.example.env .env

# Edit .env and paste your bot token
# Replace YOUR_TELEGRAM_BOT_TOKEN_HERE with your actual token
```

Your `.env` file should look like:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4. Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 Starting Tenant Maintenance AI Agent Bot...
✅ Bot is running! Press Ctrl+C to stop.
```

### 5. Test It

1. Open Telegram
2. Search for your bot username
3. Send `/start` to begin
4. Send a message like: `"Water leaking from the ceiling"`

Expected response:
```
🛠 Issue Received

Type: Plumbing Leak
Priority: HIGH
Estimated Cost: AED 1500

Status: Waiting for human approval (cost > 1000 AED)
Vendor: FastFix Plumbing
```

## Example Messages to Try

| Message | Expected Classification |
|---------|------------------------|
| "Water leaking from the ceiling" | Plumbing Leak (HIGH, 1500 AED, needs approval) |
| "AC not cooling properly" | AC Maintenance (MEDIUM, 600 AED, auto-assigned) |
| "Door handle broken" | General Maintenance (LOW, 300 AED, auto-assigned) |
| "Power outlet not working" | Electrical Issue (HIGH, 1200 AED, needs approval) |

## Project Structure

```
.
├── bot.py                  # Telegram bot - main entry point
├── mock_logic.py          # Mocked AI logic (keyword-based classification)
├── vendors.json           # Mock vendor database
├── requirements.txt       # Python dependencies
├── config.example.env     # Environment variable template
├── .env                   # Your actual config (create this, not in git)
├── .gitignore            # Keeps .env out of version control
└── README.md             # This file
```

## How It Works

1. **User sends message** → Telegram delivers to bot
2. **bot.py receives message** → Calls `mock_logic.analyze_issue(text)`
3. **mock_logic.py analyzes** → Returns classification dict
4. **bot.py formats response** → Sends back to user

### Mock Logic (Temporary)

Current classification in `mock_logic.py` uses simple keyword matching:

- Keywords like "leak", "water", "plumbing" → Plumbing Leak
- Keywords like "ac", "air", "cool" → AC Maintenance
- Keywords like "electric", "power", "light" → Electrical Issue
- Everything else → General Maintenance

**In production:** This will be replaced with:
- LLM-based natural language understanding
- Historical pattern analysis
- Dynamic cost estimation from real quotes
- Real-time vendor availability matching

## Troubleshooting

**Bot doesn't start:**
- Check that `TELEGRAM_BOT_TOKEN` is set in `.env`
- Verify the token is correct (copy-paste from BotFather)
- Make sure you ran `pip install -r requirements.txt`

**Bot doesn't respond:**
- Check the terminal for error logs
- Make sure the bot is running (`python bot.py`)
- Verify you're messaging the correct bot username

**Import errors:**
- Activate your virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## What's Next (Production Roadmap)

1. Replace mock logic with real AI agent (GPT-4, Claude, etc.)
2. Add database (PostgreSQL) for issue tracking
3. Integrate with property management systems
4. Connect to real vendor APIs for availability/pricing
5. Add web dashboard for property managers
6. SMS/WhatsApp support beyond Telegram
7. Image upload support for issue photos
8. Automated follow-up and status updates

## Demo Script for Judges

**Story:** "This is a tenant maintenance AI agent. Tenants report issues via Telegram, and our system intelligently classifies them, estimates costs, and assigns vendors automatically—unless it requires human approval."

**Live Demo:**
1. Show the bot in Telegram
2. Send: "Water is leaking in my bathroom"
3. Show the response: classified as HIGH priority, 1500 AED, needs approval
4. Send: "AC not cooling"
5. Show the response: MEDIUM priority, 600 AED, auto-assigned to vendor
6. Explain: "Right now the AI is mocked with keywords, but the architecture is ready for a real LLM agent"

## License

Demo/prototype - all rights reserved
