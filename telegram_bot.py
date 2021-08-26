import telegram


class TelegramBot:

    def __init__(self, token):
        self.token = token
        self.bot = telegram.Bot(token=self.token)

    def sendMessage(self, chat_id, message):
        self.bot.sendMessage(chat_id=chat_id, text=message)


if __name__ == "__main__":
    token = "1849234026:AAG0uAmAtJKCNi8pkjLk9qoeB-JxZwvMB5A"  # your token
    bot = TelegramBot(token)
    receiver_id = 1465659915 # your id

    bot.sendMessage(receiver_id, "Hello")