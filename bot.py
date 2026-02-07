"""
Telegram Bot for Tenant Maintenance AI Agent

This bot receives maintenance issues from tenants and responds with:
- Issue classification
- Priority level
- Estimated cost
- Assignment status (auto or needs approval)
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

import mock_logic

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🏠 **Tenant Maintenance AI Agent**

Welcome! I'm here to help with your maintenance requests.

Just describe your issue in plain text, for example:
• "Water leaking from the ceiling"
• "AC not cooling properly"
• "Door handle broken"

I'll analyze it and provide:
✓ Issue classification
✓ Priority level
✓ Cost estimate
✓ Assignment status

Go ahead and send me your maintenance issue!
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages - the main bot logic"""
    try:
        # Get the user's message
        user_text = update.message.text
        logger.info(f"Received message: {user_text}")

        # Analyze the issue using mock AI logic
        analysis = mock_logic.analyze_issue(user_text)

        # Format the response
        response = format_response(analysis)

        # Send reply to user
        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "⚠️ Sorry, something went wrong processing your request. Please try again."
        )


def format_response(analysis: dict) -> str:
    """
    Format the analysis result into a nice message for the user

    Args:
        analysis: Dict from mock_logic.analyze_issue()

    Returns:
        Formatted string message
    """
    # Build the response message
    response = "🛠 **Issue Received**\n\n"
    response += f"**Type:** {analysis['issue_type']}\n"
    response += f"**Priority:** {analysis['priority']}\n"
    response += f"**Estimated Cost:** AED {analysis['estimated_cost']}\n\n"
    response += f"**Status:** {analysis['status']}\n"

    # Add vendor info if available
    if 'vendor' in analysis and analysis['vendor']:
        if "auto-assigned" in analysis['status'].lower():
            response += f"**Vendor:** {analysis['vendor']}\n"

    return response


def main():
    """Start the bot"""
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        logger.error("Please create a .env file with your bot token.")
        logger.error("See config.example.env for template.")
        return

    logger.info("🤖 Starting Tenant Maintenance AI Agent Bot...")

    # Create the Application
    application = Application.builder().token(bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
