import random
import telebot

# Create a new Telegram bot
bot = telebot.TeleBot('6428474826:AAHxlVWbRp_Nchj6zLe4ui9dJds3KLOXO50')

# Define the game states
STATE_START = 0
STATE_CHOOSE_BAT_OR_BALL = 1
STATE_BAT = 2
STATE_BALL = 3
STATE_OUT = 4
STATE_GAME_OVER = 5

# Define the game data
current_state = STATE_START
current_score = 0
current_wickets = 0
current_batsman = None
current_bowler = None

# Define the game commands
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

@bot.message_handler(func=lambda message: current_state == STATE_BAT)
def bat(message):
    global current_score, current_wickets, current_batsman
    # Generate a random number between 0 and 6
    runs = random.randint(0, 6)
    # If the batsman scores a 0, they are out
    if runs == 0:
        current_wickets += 1
        current_batsman = None
        bot.send_message(message.chat.id, 'You are out! Your score is {}.'.format(current_score))
    # Otherwise, add the runs to the score
    else:
        current_score += runs
        bot.send_message(message.chat.id, 'You scored {} runs! Your score is now {}.'.format(runs, current_score))
    # If the batsman scores 100 runs, they are out
    if current_score >= 100:
        current_wickets += 1
        current_batsman = None
        bot.send_message(message.chat.id, 'You are out! You scored a century! Your score is {}.'.format(current_score))
    # If all 10 wickets are lost, the game is over
    if current_wickets == 10:
        current_state = STATE_GAME_OVER
        bot.send_message(message.chat.id, 'The game is over! The final score is {}.'.format(current_score))

@bot.message_handler(func=lambda message: current_state == STATE_BALL)
def ball(message):
    global current_score, current_wickets, current_batsman, current_bowler
    # Generate a random number between 0 and 6
    wickets = random.randint(0, 6)
    # If the bowler takes a wicket, the batsman is out
    if wickets == 0:
        current_wickets += 1
        current_batsman = None
        bot.send_message(message.chat.id, 'You took a wicket! The batsman is out! The score is {}.'.format(current_score))
    # Otherwise, the batsman scores a run
    else:
        current_score += 1
        bot.send_message(message.chat.id, 'The batsman scored a run! The score is now {}.'.format(current_score))
    # If all 10 wickets are lost, the game is over
    if current_wickets == 10:
        current_state = STATE_GAME_OVER
        bot.send_message(message.chat.id, 'The game is over! The final score is {}.'.format(current_score))

@bot.message_handler(func=lambda message: current_state == STATE_GAME_OVER)
def game_over(message):
    bot.send_message(message.chat.id, 'The game is already over. Start a new game by typing /start.')

if __name__ == "__main__":
    bot.polling()
