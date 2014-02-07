#This file is part product_price_by_list_price module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool
from .product import *


def register():
    Pool.register(
        ProductPriceByPriceListStart,
        Product,
        module='product_price_by_list_price', type_='model')
    Pool.register(
        ProductPriceByPriceList,
        module='product_price_by_list_price', type_='wizard')
