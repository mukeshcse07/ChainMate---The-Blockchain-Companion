import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from eliza import Eliza

# Initialize Eliza framework
eliza = Eliza(api_key="YOUR_ELIZA_API_KEY")

# Blockchain API details
BLOCKCHAIN_API_URL = "https://api.mode.network/v1"
BLOCKCHAIN_API_KEY = "YOUR_MODE_API_KEY"

# Fetch blockchain data
def get_blockchain_data():
    url = f"{BLOCKCHAIN_API_URL}/blockchain_data"
    headers = {"Authorization": f"Bearer {BLOCKCHAIN_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch data"}

# Telegram bot command handlers
def start(update, context):
    welcome_message = "Hello! I'm ChainMate, your blockchain companion. Ask me anything about blockchain!"
    update.message.reply_text(welcome_message)

def help_command(update, context):
    help_message = """
    Here's what I can do:
    - /insights: Get real-time blockchain data insights.
    - /alert <event>: Set up personalized alerts.
    - /help: Get help on using ChainMate.
    """
    update.message.reply_text(help_message)

def insights(update, context):
    data = get_blockchain_data()
    if "error" in data:
        update.message.reply_text("Unable to fetch blockchain data. Please try again later.")
    else:
        insights_message = f"Latest Blockchain Insights:\n{data}"
        update.message.reply_text(insights_message)

def handle_message(update, context):
    user_message = update.message.text
    response = eliza.chat(user_message)
    update.message.reply_text(response)

# Main function
def main():
    # Telegram bot token
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("insights", insights))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
