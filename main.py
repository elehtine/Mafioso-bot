import logging

import random
import sys

import telegram
from telegram.ext import  Updater, CommandHandler, MessageHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ROLES = [ 'ROLE 0', 'ROLE 1', 'ROLE 2', 'ROLE 3', 'ROLE 4', 'ROLE 5', 'ROLE 6', 'ROLE 7', 'ROLE 8', 'ROLE 9' ]


def start(update, context):
    """Tell all commands to user"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm bot!!!")

def new_game(update, context):
    """Create new game of mafioso"""

    # Delete old dict and create new one
    if 'mafioso' in context.bot_data:
        del context.bot_data['mafioso']
    context.bot_data['mafioso'] = list()

    # Send message for success
    context.bot.send_message(chat_id=update.effective_chat.id, text="Game created!!")

def join_game(update, context):
    """Add message sender to game"""

    # check if game is created
    if 'mafioso' not in context.bot_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Game is not created yet")
        return

    user = update.effective_user.id
    data = context.bot_data['mafioso']

    # check if already joined
    if user in data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are already joined")
        return
    data.append(user)

    # Send message for success
    context.bot.send_message(chat_id=update.effective_chat.id, text="You are added to game!!")

def begin_game(update, context):
    """Begin game and give roles to players"""

    # Check if game is created
    if 'mafioso' not in context.bot_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Game is not created yet")
        return

    # Get player roles, shuffle them and send to all players
    players = context.bot_data['mafioso']
    random.shuffle(roles)

    for player, role in zip(players, ROLES):
        context.bot.send_message(chat_id=player, text=f"Player {player} has role {role}")

    # Send message for success
    context.bot.send_message(chat_id=update.effective_chat.id, text="Roles were send")

def poll(update, context):
    """Poll answers from users"""
    print(context.bot_data)

    answers = [ "JAA", "EI", "TYHJÄ", "POISSA" ]
    question = update.message.text
    message = context.bot.send_poll(update.effective_user.id, question, answers)

    data = { message.poll.id: { "answers": answers, "message_id": message.message_id,
                                 "chat_id": update.effective_chat.id, "answers": 0 } }

    if 'poll' not in context.bot_data:
        context.bot_data['poll'] = dict()
    context.bot_data['poll'].update(data)


def help_handler(update, context):
    """Help message of bot"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="List of commands\n"
            "/start, /new, /join, /begin, /poll, /help")

def main():
    # Get token from arguments
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = "TOKEN"

    print("Your token is", token)
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('new', new_game))
    dispatcher.add_handler(CommandHandler('join', join_game))
    dispatcher.add_handler(CommandHandler('begin', begin_game))
    dispatcher.add_handler(CommandHandler('poll', poll))
    dispatcher.add_handler(CommandHandler('help', help_handler))

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
