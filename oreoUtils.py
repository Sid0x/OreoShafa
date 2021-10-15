import sys
import logging
import simplejson
import constants


def init_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(constants.LOG_FORMATTER)
    handler.setFormatter(formatter)
    root.addHandler(handler)


def read_old_items():
    old_items_file = open(constants.OLD_ITEMS_FILE_NAME,
                          constants.READ_PERMISSION)
    old_items = simplejson.load(old_items_file)
    old_items_file.close()
    return old_items


def write_old_items(new_items):
    old_items_file = open(constants.OLD_ITEMS_FILE_NAME, constants.WRITE_PERMISSION)
    simplejson.dump(new_items, old_items_file)
    old_items_file.close()


def get_product_id(item):
    id_tag = item.find(constants.SPAN,
                       class_=constants.B_TILE_ITEM_FAVORITE_INNER)
    return id_tag.attrs[constants.DATA_PRODUCT_ID]


def get_price(item):
    price_tag = item.find(constants.DIV,
                          class_=constants.B_TILE_ITEM_PRICE)
    return price_tag.text.strip()


def get_link_object(item):
    link_tag = item.find(constants.A,
                         class_=constants.B_TILE_ITEM_NAME_PRODUCT)
    link_title = link_tag.attrs[constants.TITLE]
    link_href = link_tag.attrs[constants.HREF]
    return {constants.LINK_TITLE: link_title, constants.LINK_HREF: link_href}


def get_img(item):
    img_tag = item.find(constants.IMG,
                        class_=constants.B_TILE_ITEM_IMAGE)
    return img_tag.attrs[constants.DATA_SRC]
