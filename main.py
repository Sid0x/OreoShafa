from bs4 import BeautifulSoup
from telegram import ParseMode
from oreoUtils import init_logger, read_old_items, write_old_items, get_product_id, get_price, get_link_object, get_img

import requests
import os
import telegram
import time
import random
import constants
import secretConstants
import logging


init_logger()

bot = telegram.Bot(secretConstants.TOKEN)

logging.info(constants.START_APPLICATION_OREO)

while True:
    logging.info(constants.START_SEARCH_NEW_ITEMS)

    isNewItemExist = False
    newItems = []
    oldItems = []

    if os.path.exists(constants.OLD_ITEMS_FILE_NAME) and os.stat(constants.OLD_ITEMS_FILE_NAME).st_size != 0:
        oldItems = read_old_items()

    response = requests.get(url=secretConstants.SHAFA_PARSE_URL,
                            headers=constants.HEADERS)

    shafaPageSoup = BeautifulSoup(response.text,
                                  constants.LXML)
    items = shafaPageSoup.find_all(constants.DIV,
                                   class_=constants.B_TILE_ITEM)

    for item in items:
        productId = get_product_id(item)

        newItems.append(productId)

        if len(oldItems) > 0 and productId not in oldItems:
            price = get_price(item)
            link = get_link_object(item)
            linkTitle = link[constants.LINK_TITLE]
            linkHref = link[constants.LINK_HREF]
            imgSrc = get_img(item)

            bot.sendPhoto(
                secretConstants.CHAT_ID,
                photo=imgSrc,
                caption=constants.MESSAGE.format(title=linkTitle,
                                                 price=price,
                                                 link=constants.SHAFA_URL + linkHref,
                                                 baitWord=random.choice(constants.baitWords)),
                parse_mode=ParseMode.HTML
            )
            isNewItemExist = True
            time.sleep(3)

    if not isNewItemExist:
        logging.info(constants.NEW_ITEMS_NOT_FOUND)

    write_old_items(newItems)

    logging.info(constants.WAIT_10_MIN)

    time.sleep(60 * 10)
