import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from newsapi import NewsApiClient

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

newsapi = NewsApiClient(api_key=os.environ.get("NEWS_API_KEY"))

def get_markdown_block(text, image_url):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },
        "accessory": {
            "type": "image",
            "image_url": image_url,
            "alt_text": "Image of news"
        }
    }

def get_divider_block():
    return {
        "type": "divider"
    }

@app.command("/headlines")
def handle_headlines_command(ack, respond, command, logger):
    ack()
    
    user_id = command.get("user_id")
    logger.info(f"Headlines command received from user {user_id}")
    
    headlines = newsapi.get_top_headlines(language='en', page_size=12)
    my_blocks = []
    for article in headlines['articles']:
        date, time = article['publishedAt'].split('T')
        time = time.replace('Z', '')
        line = f"*{article['title']}*\n_{date} {time}_\n> {article['description']}"
        image_url = article['urlToImage'] or "https://via.placeholder.com/150"
        my_blocks.append(get_markdown_block(line, image_url))
        my_blocks.append(get_divider_block())

    respond(blocks=my_blocks)

@app.event("message")
def handle_message_in_channel(body, say, logger):
    event = body.get("event", {})
    chan = event.get("channel", "")
    text = event.get("text", "")
    user_id = event.get("user", "")
    user = f"<@{user_id}>"
    
    logger.info(f"Received a message from user {user}: {text}, {chan}")
    if "hi " in text.lower() or "yo " in text.lower():
        say(f"Hello {user}!, try /headlines to get the latest news headlines.")


@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    logger.info("App mentioned event received")
    event = body.get("event", {})
    text = event.get("text", "")
    
    if "hello" in text.lower():
        my_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello there! :wave: I am a bot built with Block Kit.\n*How can I assist you today?*"
                }
            },
            get_divider_block(),
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "CLICK"},
                        "action_id": "button_click_action",
                        "style": "primary"  # Makes the button green
                    }
                ]
            }
        ]

        say(text="Hello from the bot!", blocks=my_blocks)

@app.action("button_click_action")
def handle_button_click(ack, body, logger, say):    
    ack()
    user_id = body["user"]["id"]
    say(f"Thanks for clicking the button, <@{user_id}>!")


# Start your app
if __name__ == "__main__":
    # Use the Socket Mode handler with your App-level Token
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()