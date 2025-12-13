# src/autotweet/cli.py
from __future__ import annotations

import sys

import tweepy

from .config import load_secrets, TWEET_LIMIT


def create_client() -> tweepy.Client:
    secrets = load_secrets()
    return tweepy.Client(
        consumer_key=secrets["TWITTER_API_KEY"],
        consumer_secret=secrets["TWITTER_API_KEY_SECRET"],
        access_token=secrets["ACCESS_TOKEN"],
        access_token_secret=secrets["ACCESS_TOKEN_SECRET"],
    )


def send_tweet(tweet_text: str) -> None:
    client = create_client()
    response = client.create_tweet(text=tweet_text)
    print(f"✅ Tweet sent! ID: {response.data['id']}")


def interactive_compose() -> str | None:
    """
    Simple REPL-like tweet composer.

    Controls:
      - Type your tweet, multiple lines allowed
      - `/send` on an empty line → finish and send
      - `/clear` → clear current text
      - `/quit` or Ctrl+D → abort without sending
    """
    print("=== Tweet composer ===")
    print("Type your tweet. Multi-line is allowed.")
    print("Commands: /send, /clear, /quit")
    print("(Ctrl+D also quits)\n")

    lines: list[str] = []

    while True:
        try:
            prompt = ">>> " if not lines else "... "
            line = input(prompt)
        except EOFError:
            print("\nAborted.")
            return None

        if line.strip() == "/quit":
            print("Aborted.")
            return None
        if line.strip() == "/clear":
            lines.clear()
            print("[cleared]")
            continue
        if line.strip() == "/send":
            tweet_text = "\n".join(lines).strip()
            if not tweet_text:
                print("⚠️  Nothing to send.")
                continue
            return tweet_text

        lines.append(line)
        tweet_text = "\n".join(lines)
        length = len(tweet_text)
        over = length - TWEET_LIMIT

        if over > 0:
            print(f"[{length} chars, {over} over {TWEET_LIMIT} ⚠️]")
        else:
            remaining = TWEET_LIMIT - length
            print(f"[{length} chars, {remaining} left]")


def main() -> None:
    # Mode 1: no args → interactive compose mode
    if len(sys.argv) == 1:
        tweet_text = interactive_compose()
        if tweet_text is None:
            return
        try:
            send_tweet(tweet_text)
        except Exception as e:
            print(f"❌ Error: {e}")
        return

    # Mode 2: with args → one-liner via CLI
    tweet_text = " ".join(sys.argv[1:])
    if not tweet_text.strip():
        print("Error: No text provided.")
        print("Usage: autotweet \"Hello World\"")
        return

    try:
        send_tweet(tweet_text)
    except Exception as e:
        print(f"❌ Error: {e}")
