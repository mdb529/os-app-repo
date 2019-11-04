from django import template
register = template.Library()

from ..models import Drug,Purchase,NDC,Contract,Manufacturer

@register.simple_tag
def get_contract_qty(self):
    return self.contract_qty(3)

@register.filter
def percentage(value):
    return format(value, ".2%")

@register.simple_tag
def get_rebate_pct(volume_tiers,volume):
    for tier in volume_tiers:
        if volume >= tier['min'] and volume <= tier['max']:
            rebate = tier['rebate']
        else:
            pass
    return rebate

@register.simple_tag
def get_rebate_amt(volume_tiers,volume,sales):
    for tier in volume_tiers:
        if volume >= tier['min'] and volume <= tier['max']:
            rebate_pct = tier['rebate']
        else:
            pass
    rebate_amt = float(rebate_pct) * float(sales)
    return rebate_amt