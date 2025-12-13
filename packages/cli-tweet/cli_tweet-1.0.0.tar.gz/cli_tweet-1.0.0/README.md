# cli-tweet

A tiny Python CLI for sending tweets/X posts from your terminal. It supports an interactive multi-line composer and a one-liner mode for quick posts.

## Requirements

- Python 3.10+
- X (Twitter) API credentials with **Read and Write** permissions

## Installation

Install from the project directory (or from a source checkout):

```bash
pip install .
```

## Credentials

The tool needs four secrets:

- `TWITTER_API_KEY` (API key under `Consumer Key`)
- `TWITTER_API_KEY_SECRET` (API secret under `Consumer Secret`)
- `ACCESS_TOKEN` (Access Token under `Authentication Tokens`)
- `ACCESS_TOKEN_SECRET` (Access Secret under `Authentication Tokens`)

Where to put them:

- Environment variables work (`export TWITTER_API_KEY=...`, etc.).
- Or create a `.env` file at the app config path (created on first run):
  - macOS/Linux default: `~/.config/cli_tweet/.env` (or `$XDG_CONFIG_HOME/cli_tweet/.env` if `XDG_CONFIG_HOME` is set).
  - You can override the directory with `CLI_TWEET_CONFIG_DIR=/custom/path`.

Example `.env`:

```env
TWITTER_API_KEY=your_key
TWITTER_API_KEY_SECRET=your_key_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

If any value is missing, `cli_tweet` will prompt for it and store it in the `.env` file (file permissions are tightened to user-only where possible).

## How to get your X API keys

1. Get a Developer Account: go to the X Developer Portal and sign up for a Free account.
2. Create a Project & App: follow the prompts to create a new Project and an associated App.
3. Set permissions (crucial):
   - Open your App settings → “User authentication settings”.
   - Select **Read and Write** permissions (not “Read” only).
   - Type of App: “Web App, Automated App or Bot”.
4. Generate keys:
   - Go to the “Keys and Tokens” tab.
   - Generate these four strings and save them immediately:
     - API Key (Consumer Key)
     - API Key Secret (Consumer Secret)
     - Access Token
     - Access Token Secret
5. Important: if you generated Access Tokens **before** switching to Read/Write, regenerate the Access Tokens. Permission level is baked into the token at creation time.

## Usage

- Interactive composer (multi-line):

  ```bash
  cli_tweet
  ```

  Controls inside the composer:

  - Type your tweet across multiple lines.
  - `/send` on an empty line sends the tweet.
  - `/clear` wipes the draft.
  - `/quit` or Ctrl+D aborts without sending.

- One-liner:
  ```bash
  cli_tweet "Hello world from the terminal"
  ```

## Notes

- Tweets are limited to 280 characters; the interactive mode shows how many characters you have left or if you are over.
- Errors from the X API (permissions, auth, etc.) are printed to the terminal so you can correct credentials or permissions quickly.
