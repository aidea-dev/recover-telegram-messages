# Telegram Deleted Message Recovery Script

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Overview

This script allows Telegram group owners to recover messages that have been accidentally deleted from their group. It leverages the Telegram Admin Log to retrieve deleted messages within **48 hours** of their deletion. After this period, the log events expire, and the messages cannot be recovered.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [License](#license)
- [Disclaimer](#disclaimer)

## Prerequisites

- **Telegram Account**: Must be the owner or have admin permissions with access to the admin log of the group.
- **Telegram API Credentials**: API ID and API Hash.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/telegram-deleted-message-recovery.git
   cd telegram-deleted-message-recovery
   ```

2. **Set up a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Obtain Telegram API Credentials**

   - Go to [my.telegram.org](https://my.telegram.org/apps).
   - Log in with your Telegram account.
   - Click on "API development tools".
   - Create a new application and note down the `API_ID` and `API_HASH`.

2. **Create a `.env` File**

   In the root directory of the project, create a file named `.env` and add the following variables:

   - **API_ID**: Your Telegram API ID.
   - **API_HASH**: Your Telegram API Hash.
   - **PHONE_NUMBER**: Your Telegram account's phone number in international format (e.g., `+123456789`).
   - **CHANNEL_NAME**: The exact name of the Telegram group/channel from which you want to recover messages.

   You can refer to the `.env_example` file as guidance for this.

## Usage

Run the script using Python:

```bash
python recover.py
```

### First-time Run Authentication

When you run the script for the first time, Telethon may prompt you for:

- **Authentication Code**: Sent to your Telegram app.
- **Two-Step Verification Password**: If you have 2FA enabled.

Follow the prompts to authenticate your session.

### Script Workflow

The script will:

- Establish a connection to your Telegram account.
- Search for the specified group/channel by name.
- Iterate through the admin log to find `DeleteMessage` events.
- Save the recovered messages to `deleted_messages.jsonl`.

## Output

- **deleted_messages.jsonl**: A JSON Lines file containing the recovered messages.

Each line represents a deleted message with the following structure:

```json
{
  "id": 123456789,
  "date": "2023-10-05T12:34:56",
  "user_id": 987654321,
  "action_type": "ChannelAdminLogEventActionDeleteMessage",
  "action": {
    "message_id": 1234,
    "message_date": "2023-10-05T12:00:00",
    "message_text": "This is the deleted message content.",
    "from_id": 123456789
  }
}
```

- **id**: Event ID from the admin log.
- **date**: Timestamp of when the deletion occurred.
- **user_id**: ID of the user who performed the deletion.
- **action_type**: Type of the admin action (`DeleteMessage`).
- **action**: Details of the deleted message.
  - **message_id**: ID of the deleted message.
  - **message_date**: Original timestamp of the message.
  - **message_text**: Content of the deleted message.
  - **from_id**: ID of the user who sent the original message.

You can refer to the `example_output.jsonl` file as an example of output.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

- Use this script responsibly and in accordance with Telegram's terms of service.
- The author is not responsible for any misuse or violation of privacy laws.
- Ensure you have the necessary permissions to access and recover messages from the group.
