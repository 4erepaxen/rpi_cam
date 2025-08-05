#!/usr/bin/env 

import time
import sys
import telepot
from picamera2 import Picamera2
from libcamera import controls
from libcamera import Transform

picam2 = Picamera2()
capture_config = picam2.create_still_configuration(transform = Transform(hflip=False, vflip=False))
picam2.start()

#picam2.set_controls({"AfMetering": controls.AfMeteringEnum.Auto})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Auto})

def handle(msg):
    global telegramText
    global chat_id
    global receiveTelegramMessage

    chat_id = msg['chat']['id']
    telegramText = msg['text']

    print("Message received from " + str(chat_id))

    if telegramText == "/start":
        bot.sendMessage(chat_id, "Camera online...")
    else:
        receiveTelegramMessage = True

def capture():
    print("Capturing photo...")

    #picam2.autofocus_cycle()
    image = picam2.switch_mode_and_capture_file(capture_config, "photo.jpg")

    print("Sending photo to " + str(chat_id))
    bot.sendPhoto(chat_id, photo = open('./photo.jpg', 'rb'))

bot = telepot.Bot('8348557916:AAHNqyrlETCEldf4Eask2dupnRi7OpuTa90')
bot.message_loop(handle)

receiveTelegramMessage = False
sendTelegramMessage = False
cameraEnable = True
sendPhoto = False

print("Telegram bot is ready")

try:
    while True:
        if receiveTelegramMessage == True:
            receiveTelegramMessage = False

            statusText = ""

            if telegramText == "/photo":
                sendPhoto = True
                statusText = "Capturing photo..."
            else:
                statusText = "Command is not valid"

            sendTelegramMessage = True

        if sendTelegramMessage == True:
            sendTelegramMessage = False
            bot.sendMessage(chat_id, statusText)

        if sendPhoto == True:
            sendPhoto = False
            capture()

except KeyboardInterrupt:
    picam2.close()
    sys.exit(0)

