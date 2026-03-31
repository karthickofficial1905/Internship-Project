from django import template
from decimal import Decimal
from ..utils import number_to_words

register = template.Library()

@register.filter
def convert_currency(value, currency='IN'):
    """Convert currency using the model's conversion method"""
    if hasattr(value, 'get_converted_price'):
        return value.get_converted_price(currency)
    elif hasattr(value, 'get_converted_unit_price'):
        return value.get_converted_unit_price(currency)
    elif hasattr(value, 'get_converted_tax_amount'):
        return value.get_converted_tax_amount(currency)
    elif hasattr(value, 'get_converted_discount'):
        return value.get_converted_discount(currency)
    elif hasattr(value, 'get_converted_total'):
        return value.get_converted_total(currency)
    elif hasattr(value, 'get_converted_total_amount'):
        return value.get_converted_total_amount(currency)
    elif hasattr(value, 'get_converted_total_tax'):
        return value.get_converted_total_tax(currency)
    elif hasattr(value, 'get_converted_total_discount'):
        return value.get_converted_total_discount(currency)
    elif hasattr(value, 'get_converted_subtotal'):
        return value.get_converted_subtotal(currency)
    return value

@register.filter
def convert_product_price(product, currency='IN'):
    """Convert product price to specified currency"""
    if hasattr(product, 'get_converted_price'):
        return product.get_converted_price(currency)
    return product.rate if hasattr(product, 'rate') else 0

@register.filter
def convert_item_unit_price(item, currency='IN'):
    """Convert item unit price to specified currency"""
    if hasattr(item, 'get_converted_unit_price'):
        return item.get_converted_unit_price(currency)
    return item.unit_price if hasattr(item, 'unit_price') else 0

@register.filter
def convert_item_tax(item, currency='IN'):
    """Convert item tax amount to specified currency"""
    if hasattr(item, 'get_converted_tax_amount'):
        return item.get_converted_tax_amount(currency)
    return item.tax_amount if hasattr(item, 'tax_amount') else 0

@register.filter
def convert_item_discount(item, currency='IN'):
    """Convert item discount to specified currency"""
    if hasattr(item, 'get_converted_discount'):
        return item.get_converted_discount(currency)
    return item.discount if hasattr(item, 'discount') else 0

@register.filter
def convert_item_total(item, currency='IN'):
    """Convert item total to specified currency"""
    if hasattr(item, 'get_converted_total'):
        return item.get_converted_total(currency)
    return item.total if hasattr(item, 'total') else 0

@register.filter
def convert_invoice_total_amount(invoice, currency='IN'):
    """Convert invoice total amount to specified currency"""
    if hasattr(invoice, 'get_converted_total_amount'):
        return invoice.get_converted_total_amount(currency)
    return invoice.total_amount if hasattr(invoice, 'total_amount') else 0

@register.filter
def convert_invoice_total_tax(invoice, currency='IN'):
    """Convert invoice total tax to specified currency"""
    if hasattr(invoice, 'get_converted_total_tax'):
        return invoice.get_converted_total_tax(currency)
    return invoice.total_tax if hasattr(invoice, 'total_tax') else 0

@register.filter
def convert_invoice_total_discount(invoice, currency='IN'):
    """Convert invoice total discount to specified currency"""
    if hasattr(invoice, 'get_converted_total_discount'):
        return invoice.get_converted_total_discount(currency)
    return invoice.total_discount if hasattr(invoice, 'total_discount') else 0

@register.filter
def convert_invoice_subtotal(invoice, currency='IN'):
    """Convert invoice subtotal to specified currency"""
    if hasattr(invoice, 'get_converted_subtotal'):
        return invoice.get_converted_subtotal(currency)
    return invoice.subtotal if hasattr(invoice, 'subtotal') else 0

@register.filter
def convert_cart_subtotal(cart, currency='IN'):
    """Convert cart subtotal to specified currency"""
    if hasattr(cart, 'get_converted_subtotal'):
        return cart.get_converted_subtotal(currency)
    return cart.subtotal if hasattr(cart, 'subtotal') else 0

@register.filter
def convert_cart_total_discount(cart, currency='IN'):
    """Convert cart total discount to specified currency"""
    if hasattr(cart, 'get_converted_total_discount'):
        return cart.get_converted_total_discount(currency)
    return cart.total_discount if hasattr(cart, 'total_discount') else 0

@register.filter
def convert_cart_grand_total(cart, currency='IN'):
    """Convert cart grand total to specified currency"""
    if hasattr(cart, 'get_converted_grand_total'):
        return cart.get_converted_grand_total(currency)
    return cart.grand_total if hasattr(cart, 'grand_total') else 0

@register.filter
def convert_cart_item_gst(item, currency='IN'):
    """Convert cart item GST amount to specified currency"""
    if hasattr(item, 'get_converted_gst_amount'):
        return item.get_converted_gst_amount(currency)
    return item.gst_amount if hasattr(item, 'gst_amount') else 0

@register.filter
def convert_cart_item_total(item, currency='IN'):
    """Convert cart item total price to specified currency"""
    if hasattr(item, 'get_converted_total_price'):
        return item.get_converted_total_price(currency)
    return item.total_price if hasattr(item, 'total_price') else 0

@register.filter
def amount_to_words(amount, country_code='IN'):
    """Convert amount to words based on country currency"""
    return number_to_words(amount, country_code)