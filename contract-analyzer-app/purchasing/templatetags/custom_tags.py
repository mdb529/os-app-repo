from django import template
register = template.Library()

from ..models import Drug,Purchase,NDC

@register.simple_tag
def get_contract_qty(self):
    return self.contract_qty(3)