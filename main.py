import telebot
import requests
import json
import pickle
from web3 import Web3
from mnemonic import Mnemonic
from moralis import evm_api

infura = process.env(Api_Key)
w3 = Web3(Web3.HTTPProvider(infura))

bot = telebot.TeleBot(Api_key)
public_key = ""
#allowed = [795341146]
addy_cache = 'addy.pickle'
file_name = 'cached_array.pickle'
#addyVerified = []


def cache_data(data, file_name):
  with open(file_name, 'wb') as f:
    pickle.dump(data, f)


def load_cached_data(file_name):
  try:
    with open(file_name, 'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    return None


#cache_data(allowed, file_name)
#cache_data(addyVerified, addy_cache)

verifiedAddyCache = load_cached_data(addy_cache)
allowed = load_cached_data(file_name)


@bot.message_handler(commands=["start"])
def start(message):
  bot.send_photo(
    message.chat.id,
    "https://ibb.co/V3ysYTq",
    caption=
    f"<i><b>Hey Welcome To Whale Chat Bot</b>.\n\n<tg-spoiler>use /verify to verify you're a whale and get acess to the private chat</tg-spoiler></i>",
    parse_mode="html")






bot.polling()
