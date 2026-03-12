import os
from dotenv import load_dotenv

load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("message")
def handle_message_in_channel(body, say, logger):    
    print(body)
    chan = body.get("channel", {}).get("id", "")
    event = body.get("event", {})
    text = event.get("text", "")
    user_id = event.get("user", "")
    user = f"<@{user_id}>"
    
    #logger.info(f"Received a message from user {user}: {text}, {chan}")
    say(f"Hello {user}, you said: {text}")


@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    print("App mentioned event received")
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
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "CLICK"
                        },                        
                        "action_id": "button_click_action",
                        "style": "primary" # Makes the button green
                    }
                ]
            }
        ]
               
        say(text="Hello from the bot!", blocks=my_blocks)

# Listen for a click on a button with the action_id "button_click_action"
@app.action("button_click_action")
def handle_button_click(ack, body, logger, say):
    # Acknowledge the action right away. Slack requires you to acknowledge 
    # interactions within 3 seconds, or the user will see an error.
    ack()
    
    # Extract the user ID who clicked the button
    user_id = body["user"]["id"]
    say(f"Thanks for clicking the button, <@{user_id}>!")



# Start your app
if __name__ == "__main__":
    # Use the Socket Mode handler with your App-level Token
    # This is the xapp- token
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()