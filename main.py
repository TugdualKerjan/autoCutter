import cv2
from predictor import predict

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
import numpy as np
import os
from io import BytesIO
token = os.environ['TOKEN']
updater = Updater(token=token, use_context=True)

def resize(image):
    height, width, _ = image.shape
    percent = (width / 512)
    dim = (512, int(height / percent))
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    height, width, _ = resized.shape
    if height < 512:
        return resized
    else:
        resized = resized[:512, :] #Truncate the height
        return resized

def main():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, receive_images))
    dispatcher.add_handler(MessageHandler(Filters.sticker, receive_stickers))

    updater.start_polling()

def receive_stickers(update, context):
    context.bot.deleteStickerFromSet(update.message.sticker['file_id'])

def receive_images(update, context):
    user_id = int(update.message.from_user['id'])
    username = update.message.from_user['username']

    decode_img = cv2.imdecode(np.frombuffer(BytesIO(context.bot.getFile(update.message.photo[-1].file_id).download_as_bytearray()).getbuffer(), np.uint8), -1)
    context.bot.sendMessage(update.effective_chat.id, "Preparing scissors and glue...")
    context.bot.send_photo(740175095, update.message.photo[-1].file_id)
    
    for subimage in predict(decode_img):
        subimage = resize(subimage)
        buffer = cv2.imencode(".png", subimage)[1].tobytes()
        try: 
            context.bot.add_sticker_to_set(user_id, name="pepites_de_%s_by_stickerspeedrunner_bot" % username, emojis="🧮", png_sticker=buffer)
        except:
            context.bot.createNewStickerSet(user_id, name="pepites_de_%s_by_stickerspeedrunner_bot" % username, title="PepitesDe%sSticker" % username, png_sticker=buffer, emojis="🙂")
        context.bot.sendSticker(update.effective_chat.id, buffer)
    context.bot.sendMessage(update.effective_chat.id, "Get your stickers at t.me/addstickers/pepites_de_%s_by_stickerspeedrunner_bot" % username)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Hey! Send me a message with a picture and I'll cut it out for you!""")


if __name__ == '__main__':
    main()