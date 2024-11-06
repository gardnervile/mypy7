import os
from dotenv import load_dotenv
from pytimeparse import parse
import ptbot


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f'{prefix} |{pbar}| {percent}% {suffix}'


def wait(bot, chat_id, delay):
    message_id = bot.send_message(chat_id, f"Осталось {delay} секунд")
    bot.create_countdown(delay, notify_progress, bot=bot, chat_id=chat_id, message_id=message_id, total=delay)
    bot.create_timer(delay, send_timeout_message, bot=bot, chat_id=chat_id)


def notify_progress(secs_left, bot, chat_id, message_id, total):
    progress_bar = render_progressbar(total, total - secs_left, prefix='Прогресс:', suffix='завершено')
    bot.update_message(chat_id, message_id, f"Осталось {secs_left} секунд\n{progress_bar}")


def on_message(bot, chat_id, message):
    delay = parse(message)
    if delay is not None:
        wait(bot, chat_id, delay)


def send_timeout_message(bot, chat_id):
    bot.send_message(chat_id, "Время вышло!")


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda chat_id, message: on_message(bot, chat_id, message))
    bot.run_bot()


if __name__ == '__main__':
    main()
