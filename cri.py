#New cricket script

import random
import telebot
import time

bot = telebot.TeleBot('YOUR_BOT_TOKEN')

STATE_START = 0
STATE_CHOOSE_BAT_OR_BALL = 1
STATE_BAT = 2
STATE_BALL = 3
STATE_OUT = 4
STATE_GAME_OVER = 5

current_state = STATE_START
current_score = 0
current_wickets = 0
current_batsman = None
current_bowler = None

MAX_OVERS = 4
innings_count = 1
current_over = 0
current_ball = 0

@bot.message_handler(commands=['start'])
def start_game(message):
    global current_state, current_score, current_wickets, current_batsman, current_bowler
    current_state = STATE_CHOOSE_BAT_OR_BALL
    current_score = 0
    current_wickets = 0
    current_batsman = None
    current_bowler = None
    bot.send_message(message.chat.id, 'Welcome to the Telegram cricket game! Do you want to bat or ball first?')

@bot.message_handler(func=lambda message: current_state == STATE_CHOOSE_BAT_OR_BALL)
def choose_bat_or_ball(message):
    global current_state, current_batsman, current_bowler
    if message.text == 'bat':
        current_state = STATE_BAT
        current_batsman = message.from_user.id
        bot.send_message(message.chat.id, 'You have chosen to bat first. Your score is currently 0.')
    elif message.text == 'ball':
        current_state = STATE_BALL
        current_bowler = message.from_user.id
        bot.send_message(message.chat.id, 'You have chosen to ball first. The batsman is currently on 0.')
    else:
        bot.send_message(message.chat.id, 'Please choose either "bat" or "ball".')

@bot.message_handler(func=lambda message: current_state == STATE_BAT or current_state == STATE_BALL)
def play_game(message):
    global current_over, current_ball
    if innings_count > 2:
        bot.send_message(message.chat.id, 'Match is over. Thanks for playing!')
        return

    if current_ball == 6:
        current_over += 1
        current_ball = 0

    if current_over == MAX_OVERS:
        bot.send_message(message.chat.id, 'Innings {} is over!'.format(innings_count))
        innings_count += 1
        current_over = 0
        current_ball = 0
        switch_roles()
        return

    if current_state == STATE_BAT:
        bat(message)
    elif current_state == STATE_BALL:
        ball(message)

def switch_roles():
    global current_state, current_batsman, current_bowler
    current_batsman, current_bowler = current_bowler, current_batsman
    current_state = STATE_BAT if current_state == STATE_BALL else STATE_BALL

def send_message_with_delay(chat_id, message, delay=1):
    time.sleep(delay)
    bot.send_message(chat_id, message)

def bat(message):
    global current_score, current_wickets, current_batsman
    runs = random.randint(0, 6)
    if runs == 0:
        current_wickets += 1
        current_batsman = None
        bot.send_message(message.chat.id, 'You are out! Your score is {}.'.format(current_score))
    else:
        current_score += runs
        bot.send_message(message.chat.id, 'You scored {} runs! Your score is now {}.'.format(runs, current_score))
    if current_score >= 100:
        current_wickets += 1
        current_batsman = None
        bot.send_message(message.chat.id, 'You are out! You scored a century! Your score is {}.'.format(current_score))
    if current_wickets == 10:
        current_state = STATE_GAME_OVER
        bot.send_message(message.chat.id, 'The game is over! The final score is {}.'.format(current_score))

def ball(message):
    global current_score, current_wickets, current_batsman, current_bowler
    wickets = random.randint(0, 6)
    if wickets == 0:
        current_wickets += 1
        current_batsman = None
        bot.send_message(message.chat.id, 'You took a wicket! The batsman is out! The score is {}.'.format(current_score))
    else:
        current_score += 1
        bot.send_message(message.chat.id, 'The batsman scored a run! The score is now {}.'.format(current_score))
    if current_wickets == 10:
        current_state = STATE_GAME_OVER
        bot.send_message(message.chat.id, 'The game is over! The final score is {}.'.format(current_score))

  if __name__ == "__main__":
    bot.polling()
