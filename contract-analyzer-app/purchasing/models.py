from django.db import models
from django.contrib.postgres.fields import JSONField
import json 
from pprint import pprint
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify


class Manufacturer(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    slug = models.SlugField()
    logo_img= models.ImageField(upload_to="logos/",blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Drug(models.Model):
    
    name = models.CharField(max_length=100, primary_key=True)
    slug = models.SlugField()
    manufacturer= models.ForeignKey(Manufacturer, on_delete=models.CASCADE, to_field='name',related_name='drugs')
    route_type= models.CharField(max_length=10,blank=True, null=True)
    cpt_dosage= models.CharField(max_length=100,blank=True, null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Drug, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class NDC(models.Model):
    class Meta:
        verbose_name = 'NDC'
        verbose_name_plural = 'NDCs'

    drug_name= models.ForeignKey(Drug, on_delete=models.CASCADE, to_field='name', related_name='ndcs')
    ndc_code= models.CharField(max_length=13, primary_key=True)
    hcpcs_code= models.CharField(max_length=5,blank=True, null=True)
    numerator_strength= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    cpt_mbu= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_package= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    package_qty= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_ndc= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    ndc_unit_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.drug_name} | {self.ndc_code} | {self.numerator_strength}"
    
class Contract(models.Model):

    CONTRACT_TYPES = (
        ('G','Growth'),
        ('V','Volume'),
        ('MS','Market Share'),
        ('P', 'Portfolio'),
        ('VG','Volume/Growth'),
        ('GMS', 'Growth/Market Share'),
        ('GP', 'Growth/Portfolio'),
        ('VMS', 'Volume/Market Share'),
        ('VMS', 'Volume/Market Share'),
    )
    

    drug_name= models.OneToOneField(Drug, on_delete=models.CASCADE, to_field='name')
    manufacturer= models.ForeignKey(Manufacturer, on_delete=models.CASCADE, to_field='name',related_name='contracts')
    drug_category= models.CharField(max_length=10, blank=True, null=True)
    measured_equivalents_qty= models.DecimalField(max_digits=15,decimal_places=4,blank=True, null=True)
    measured_equivalents_unit= models.CharField(max_length=10, blank=True, null=True)
    contract_type= models.CharField(choices=CONTRACT_TYPES, max_length=50,blank=True, null=True)
    effective_start_date= models.DateField(blank=True, null=True)
    effective_end_date= models.DateField(blank=True, null=True)
    baseline_start_date= models.DateField(blank=True, null=True)
    baseline_end_date= models.DateField(blank=True, null=True)
    baseline_measure= models.CharField(max_length=50, blank=True, null=True)
    rebate_schedule= JSONField(blank=True, null=True)

    def get_contract_qty(self):
        if self.measured_equivalents_qty == 1 & self.measured_equivalents_unit == 'BOTTLE':
            self.contract_qty = SUM(self.delivered_qty)
            return self.contract_qty
        else:
            self.contract_qty = SUM(self.extended_delivered_qty) / self.measured_equivalents_qty
            return self.contract_qty

    def __str__(self):
        return f"Contract: {self.drug_name} Manufacturer: {self.manufacturer} Drug Category: {self.drug_category} Measured Equivalents: {self.measured_equivalents_qty}"

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