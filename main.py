import cv2
from predictor import predict

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
import numpy as np
from io import BytesIO

updater = Updater(token='1607764973:AAHe1HbFf1JWYBUQUlPshRoOuUNng0fObvw', use_context=True)

def resize(image):
    height, width, _ = image.shape
    if width < 512:
        if height < 512:
            return image
        else:
            image = image[:512, :] #Truncate the height
            return image

    else:
        percent = (width / 512)
        dim = (512, int(height / percent))
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        height, width, _ = resized.shape
        if height < 512:
            return resized
        else:
            return resized[:512, :] #Truncate the height

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


    file = context.bot.getFile(update.message.photo[-1].file_id)
    f =  BytesIO(file.download_as_bytearray())
    decode_img = cv2.imdecode(np.frombuffer(f.getbuffer(), np.uint8), -1)
    
    for subimage in predict(decode_img):
        subimage = resize(subimage)
        buffer = cv2.imencode(".png", subimage)[1].tobytes()
        try: 
            print("Adding to sticker pack")
            print(context.bot.add_sticker_to_set(user_id, name="pepites_de_%s_by_faststicker_bot" % username, emojis="🧮", png_sticker=buffer))
            context.bot.sendSticker(update.effective_chat.id, buffer)
        except:
            print("Can't find sticker pack")
            context.bot.createNewStickerSet(user_id, name="pepites_de_%s_by_faststicker_bot" % username, title="PepitesDe%s" % username, png_sticker=buffer, emojis="🙂")
    context.bot.sendMessage(update.effective_chat.id, "Get your stickers at t.me/addstickers/pepites_de_%s_by_faststicker_bot" % username)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Hey! Send me a message with a picture and I'll cut it out for you!""")


if __name__ == '__main__':
    main()