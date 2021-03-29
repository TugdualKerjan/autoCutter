# Cut out stickers for Telegram automatically!

Thanks to detectron2 and the python-telegram-bot library one can detect people in images and cut them out!

## How it works:

- Add the bot on telegram using this link: https://t.me/faststicker_bot

- Send him the picture you desire to cut

- See the magic happen

## Development:

Around 10h of work to get it to work, mainly understanding how Heroku deals with python packages and adding a build thingy to install lib that was missing for opencv.

- A lot of work to try and get a more efficient and less costly version mask_rcnn using vovnet, unfortunately Heroku still didn't want to go above 500MB limit of memory usage.
- Lots of work to understand how to generate and add sticker packs that would be personal to each user on the platform.
- Some attemps made to get it to work using a Dockerfile, which was a success but uploading an image failed, dockerhub is bull for that.