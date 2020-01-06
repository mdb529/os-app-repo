from django import template
from decimal import Decimal
import locale
locale.setlocale(locale.LC_ALL, '')
register = template.Library()
 
 
# @register.filter()
# def currency(value):
#     return locale.currency(value, grouping=True)

@register.filter(name='currency')    
def currency(value):    
    try:    
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')    
    except:    
        locale.setlocale(locale.LC_ALL,'')    
    value = Decimal(value)    
    loc = locale.localeconv()    
    return locale.currency(value, loc['currency_symbol'], grouping=True)