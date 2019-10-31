from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import (ExtractYear,ExtractQuarter,ExtractMonth,ExtractDay)
from os_contracts.models import Drug, Contract, NDC, Manufacturer



class Transaction(models.Model):
    os_account_id = models.CharField(max_length=6, blank=True, null=True)
    drug_name = models.CharField(max_length=100, blank=True, null=True)
    ndc_code = models.ForeignKey(NDC, on_delete=models.CASCADE, to_field='ndc_code', blank=True, null=True, related_name='transactions')
    hcpcs_code = models.CharField(max_length=100, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    item_description = models.CharField(max_length=100, blank=True, null=True)
    ordered_qty = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    delivered_qty = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    backordered_qty = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    order_status = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    awp = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    billing_unit = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    billing_unit_price = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    billing_units_per_package = models.CharField(max_length=100, blank=True, null=True)
    asp_per_billing_unit = models.CharField(max_length=100, blank=True, null=True)
    is_credit = models.BooleanField()
    route_of_administration_description = models.CharField(max_length=100, blank=True, null=True)
    mbus_per_ndc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    ndc_unit_sum = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    extended_ordered_qty = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    extended_delivered_qty = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)






    def __str__(self):
        return f"{self.invoice_date} | {self.drug_name} | {self.delivered_qty} | {self.extended_delivered_qty}"
