import telebot
import requests
import json
import pickle
from web3 import Web3
from mnemonic import Mnemonic
from moralis import evm_api

moralis_key = "GFe9A3lNYWFSv1jO5NmC14bUHeW4oedryp1BPUHxAnAMZUL7C3Nd0Ppjaru3003R"
Api_key = "5964876840:AAHe5gbeYg9e1BtPIX2WJauspGbwWd1i1Ao"
infura = "https://mainnet.infura.io/v3/c1f653384020470d942fdd4d8eb97795"
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


@bot.message_handler(commands=["verify"])
def verify(message):
  global public_key
  if message.chat.id in allowed:
    bot.send_animation(
      message.chat.id,
      animation="https://media.giphy.com/media/Y07F3fs9Is5byj4zK8/giphy.gif",
      caption=f"<b>You're Already Verified :) </b>\n",
      parse_mode="html")
  else:
    url = f"https://api.telegram.org/bot{Api_key}/getUpdates"
    print(url)
    #chat_id = latest_message["message"]["chat"]["id"]
    #print(chat_id)
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=256)
    seed = mnemo.to_seed(words, passphrase="")
    account = w3.eth.account.privateKeyToAccount(seed[:32])
    private_key = account.privateKey
    public_key = account.address
    private_key = private_key.hex()
    #public_key = int(public_key)
    bot.send_message(message.chat.id,
                     f"<b><i>{public_key}</i></b>",
                     parse_mode="html")
    sent_msg = bot.send_message(
      message.chat.id,
      f"<b><i>To Get Verified And Access To The bot Make Sure You Have more than 1% of supply.\n\nIf you have then copy the above wallet address and send 0.0001 bnb  to that address. \n\nThen send a msg with /hashVerify with your transaction hash </i></b> ",
      parse_mode="html",
    )


@bot.message_handler(commands=['hashVerify'])
def hashVerify(message):
  if message.chat.id in allowed:
    bot.send_animation(
      message.chat.id,
      animation="https://media.giphy.com/media/Y07F3fs9Is5byj4zK8/giphy.gif",
      caption=f"<b>You're Already Verified :) </b>",
      parse_mode="html")
  if message.chat.id not in allowed:
    if public_key == "":
      bot.send_message(
        message.chat.id,
        f"<b><i> Use /verify first and get a wallet address</i></b>",
        parse_mode="html")
    else:
      txHash = message.text.split(" ")[1]
      print(txHash)
      if txHash.startswith("0x"):
        print("hi")
        checkTxHash(txHash, message)

      if txHash.startswith("http"):
        newTx = txHash.split("/")[4]
        checkTxHash(newTx, message)
      else:
        bot.send_message(
          message.chat.id,
          f"<b><i>The tx hash you sent is incorrect try again !! </i></b>",
          parse_mode="html")


def checkTxHash(tx, message):
  global verifiedAddyCache
  global allowed
  global ourTokenCa
  global public_key
  params = {
    "transaction_hash": tx,
    "chain": "bsc",
  }
  result = evm_api.transaction.get_transaction(
    api_key=moralis_key,
    params=params,
  )
  fromAddy = result['from_address']
  toAddy = result['to_address']
  toAddy = toAddy.lower()
  public_key = public_key.lower()
  if toAddy == public_key and fromAddy not in verifiedAddyCache:
    urlCheck = ("https://api.bscscan.com/api"
                "?module=account"
                "&action=tokenbalance"
                f"&contractaddress={ourTokenCa}"
                f"&address={fromAddy}"
                "&tag=latest"
                "&apikey=JIW519CDP82K5S9QU9JFN8CPP8TRFSWXT7")
    response = requests.get(urlCheck)
    datac = response.text
    balance = json.loads(datac)['result']
    if balance > 100000:
      print(allowed)
      id = int(message.chat.id)
      bot.send_animation(
        message.chat.id,
        animation="https://media.giphy.com/media/Y07F3fs9Is5byj4zK8/giphy.gif",
        caption=f"<b>Yayy!! Congrats You're  Verified :) </b>",
        parse_mode="html")
      allowed.append(id)
      verifiedAddyCache.append(fromAddy)
      bot_id = 795341146
      print(bot_id)
      bot.send_message(bot_id,
                       f"User Verified {message.chat.id},\nAddy = {fromAddy}")
      cache_data(allowed, file_name)
      cache_data(verifiedAddyCache, addy_cache)
      url = f"https://api.telegram.org/bot{Api_key}/createChatInviteLink"
      params = {'chat_id': -1001783361291, 'member_limit': 1}
      res = requests.get(url, params)
      link = res.json()
      linki = link['result']['invite_link']
      bot.send_message(message.chat.id, f"{linki}")
    else:
      bot.send_message(
        message.chat.id,
        "<b>You dont have sufficent Tokens</b><i>Buy Now MF</i>",
        parse_mode="html")
  else:
    bot.send_message(message.chat.id,
                     "<b>You're TX Dosent match try again</b>",
                     parse_mode="html")


bot.polling()
