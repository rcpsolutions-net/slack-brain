# slack-brain

A Slack bot built with [Slack Bolt for Python](https://slack.dev/bolt-python/) that brings news headlines and interactive messaging into your Slack workspace. More features to come...

## Features

- **`/headlines`** — Fetches the top 12 English news headlines via [NewsAPI](https://newsapi.org/) and posts them as formatted Slack Block Kit messages with images, titles, and publish timestamps.
- **Greeting responder** — Listens for messages containing "hi" or "yo" and replies with a friendly prompt to try `/headlines`.
- **App mention handler** — When you `@mention` the bot and say "hello", it replies with an interactive Block Kit message.
- **Button interaction** — Handles button clicks from Block Kit messages and acknowledges the user.

## Prerequisites

- Python 3.12+
- A [Slack App](https://api.slack.com/apps) with Socket Mode enabled
- A [NewsAPI](https://newsapi.org/) account and API key

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd slack-brain
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install slack-bolt newsapi-python python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-level-token
NEWS_API_KEY=your-newsapi-key
```

| Variable | Where to find it |
| --- | --- |
| `SLACK_BOT_TOKEN` | Slack App > OAuth & Permissions > Bot User OAuth Token |
| `SLACK_APP_TOKEN` | Slack App > Basic Information > App-Level Tokens (requires `connections:write` scope) |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org/) > Account dashboard |

### 4. Configure your Slack App

In your [Slack App settings](https://api.slack.com/apps):

- **Socket Mode**: Enable it under *Settings > Socket Mode*
- **Event Subscriptions**: Subscribe to `message.channels` and `app_mention` bot events
- **Slash Commands**: Add a `/headlines` command
- **Interactivity**: Enable it to support button clicks

### 5. Run the bot

```bash
python app.py
```

## Project Structure

```text
slack-brain/
├── app.py        # Main bot logic
├── .env          # Environment variables (not committed)
└── README.md
```

## Tech Stack

- [Slack Bolt for Python](https://slack.dev/bolt-python/) — Slack app framework
- [NewsAPI Python Client](https://newsapi.org/docs/client-libraries/python) — News headlines
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management
