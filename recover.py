from telethon.sync import TelegramClient
from telethon.tl.types import *
import json
from dotenv import load_dotenv

# Load environment variables from .env file
# Please refer to the README.md file for more information
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
channel_id = int(os.getenv("CHANNEL_ID"))
channel_name = os.getenv("CHANNEL_NAME")


def serialize_event(event):
    """
    The function `serialize_event` serializes a Telegram admin log event object into a dictionary format.

    :param event: this dictionary contains information about the event such as id, date, user_id,
    action_type, and specific details based on the type of action associated with the event

    :return: a serializable dictionary with the event information if the event is a DeleteMessage action,
    otherwise, it returns None
    """

    event_dict = {
        "id": event.id,
        "date": event.date.isoformat(),
        "user_id": event.user_id,
        "action_type": event.action.__class__.__name__,
        "action": {},
    }

    action = event.action

    if isinstance(action, ChannelAdminLogEventActionDeleteMessage):
        message = action.message
        event_dict["action"] = {
            "message_id": message.id,
            "message_date": message.date.isoformat(),
            "message_text": message.message,
            "from_id": message.from_id.user_id if message.from_id else None,
        }
    else:
        # We leave blank for events that are different from the DeleteMessage action
        event_dict = None

    # Eventually, other types can be handled in a similar way
    # elif isinstance(action, ChannelAdminLogEventActionParticipantJoin):
    #    event_dict["action"] = {
    #        "user_id": event.user_id,
    #        "action": "participant_joined",
    #    }

    return event_dict


async def main():
    async with TelegramClient("recovery_session", api_id, api_hash) as client:

        # Iterate over all the chats the user is in
        # and find the chat with the specified name
        id = None
        async for dialog in client.iter_dialogs():

            if dialog.name == channel_name:
                id = dialog.entity.id
                break

        # We use the channel id to get the channel object
        if id:
            channel = await client.get_entity(id)
            print("Chat found. Starting event collection...")
        else:
            print("Chat not found. Exiting.")
            return

        with open("deleted_messages.jsonl", "w", encoding="utf-8") as f:

            count = 0
            async for event in client.iter_admin_log(channel):
                try:
                    event_dict = serialize_event(event)

                    if event_dict:  # If the event is a DeleteMessage action
                        f.write(json.dumps(event_dict, ensure_ascii=False) + "\n")

                except Exception as e:
                    print(f"Error serializing event {event.id}: {e}")

                count += 1

                print(f"Events collected: {count}", end="\r", flush=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
