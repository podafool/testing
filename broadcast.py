import telegram

class TelegramBroadcaster:
    def __init__(self, api_key):
        self.bot = telegram.Bot(api_key)

    def broadcast(self, message, group_id):
        """Broadcasts a message to a Telegram group.

        Args:
            message: The message to broadcast.
            group_id: The ID of the Telegram group.
        """

        for member in self.bot.get_chat_members(group_id):
            self.bot.send_message(member.id, message)

if __name__ == '__main__':
    api_key = 'YOUR_API_KEY'
    broadcaster = TelegramBroadcaster(api_key)

    # Get the ID of the Telegram group to broadcast to.
    group_id = 'YOUR_GROUP_ID'

    # Broadcast the message.
    broadcaster.broadcast('This is a broadcast message!', group_id)
