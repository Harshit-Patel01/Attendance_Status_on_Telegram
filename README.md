# Cyber Vidya Attendance Bot

This is an automated bot that checks your attendance on the CyberVidya platform and sends you a notification via Telegram if there are any changes.

The bot is designed to run automatically every 15 minutes using GitHub Actions.

## How It Works

The script logs into the CyberVidya portal, fetches your current attendance for all registered courses, and compares it with the last known state (stored in `attendance_state.json`). If any attendance figures have changed, it calculates the new percentage and sends a detailed message to your specified Telegram chat.

The entire process is automated using a GitHub Actions workflow, which is scheduled to run every 15 minutes. The updated attendance state is committed back to the repository after each run to ensure persistence.

## Setup

To use this bot for your own account, follow these steps:

1.  **Fork this repository** to your own GitHub account.

2.  **Set up Repository Secrets**: For the bot to access your credentials securely, you must add them as secrets in your forked repository.
    *   Go to your repository's **Settings** > **Secrets and variables** > **Actions**.
    *   Click **New repository secret** and add the following four secrets:

| Secret Name | Description |
| :--- | :--- |
| `USERNAME` | Your CyberVidya username. |
| `PASSWORD` | Your CyberVidya password. |
| `BOT_TOKEN` | Your Telegram bot token. |
| `CHAT_ID` | The chat ID for the Telegram user or group to receive notifications. |

3.  **Enable GitHub Actions**: If they are not already enabled, go to the **Actions** tab of your repository and enable them.

That's it! The bot will now run automatically. You can also trigger a run manually from the Actions tab by selecting the "Check Attendance" workflow and clicking "Run workflow".
