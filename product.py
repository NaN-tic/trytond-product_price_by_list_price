#This file is part product_price_by_list_price module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from decimal import Decimal
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateView, StateTransition, StateAction, \
    Button
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, If, PYSONEncoder
from trytond.transaction import Transaction

__all__ = ['ProductPriceByPriceListStart', 'ProductPriceByPriceList', 'Product']
__metaclass__ = PoolMeta


class ProductPriceByPriceListStart(ModelView):
    'Product Price By Price List'
    __name__ = 'product.price.by.list_price.start'
    price_list = fields.Many2One('product.price_list', 'Price List',
            required=True)
    customer = fields.Many2One('party.party', 'Customer')


class ProductPriceByPriceList(Wizard):
    'Product Price By Price List'
    __name__ = 'product.price.by_price_list'
    start = StateView('product.price.by.list_price.start',
        'product_price_by_list_price.product_price_by_list_price_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Get prices', 'open', 'tryton-ok', default=True),
            ])
    open = StateAction('product_price_by_list_price.act_product_price_by_list_price_tree')

    def do_open(self, action):
        price_list = self.start.price_list

        context = {}
        context['price_list'] = self.start.price_list.id
        context['customer'] = self.start.customer and self.start.customer.id or None
        action['pyson_context'] = PYSONEncoder().encode(context)
        action['name'] += ' - %s' % (price_list.rec_name)
        return action, {}


class Product:
    __name__ = 'product.product'
    price_x1 = fields.Function(fields.Numeric('Price x1'),
        'price_by1')

    @classmethod
    def get_price_by_price_list(self, products, quantity=1):
        prices = {}
        context = {}

        with Transaction().set_context(context):
            prices = self.get_sale_price(products, quantity)
        return prices

    @classmethod
    def price_by1(self, products, name):
        return self.get_price_by_price_list(products, quantity=1)
