from django.db import models



class Transaction(models.Model):
    os_account_id = models.CharField(max_length=6, blank=True, null=True)
    os_account = models.CharField(max_length=100, blank=True, null=True)
    drug_name = models.CharField(max_length=100, blank=True, null=True)
    ndc_code = models.CharField(max_length=13, blank=True, null=True)
    hcpcs_code = models.CharField(max_length=100, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    item_description = models.CharField(max_length=100, blank=True, null=True)
    ordered_quantity = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    delivered_quantity = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    backordered_quantity = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    order_status = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    awp = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    billing_unit = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    billing_unit_price = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    billing_units_per_package = models.CharField(max_length=100, blank=True, null=True)
    asp_per_billing_unit = models.CharField(max_length=100, blank=True, null=True)
    is_credit = models.BooleanField()
    route_of_administration_code_description = models.CharField(max_length=100, blank=True, null=True)
    mbus_per_ndc = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    units_of_service = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    extended_ordered_qty = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    extended_delivered_qty = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)




    def __str__(self):
        return f"{self.invoice_date} | {self.drug_name} | {self.delivered_quantity} | {self.extended_delivered_qty}"
