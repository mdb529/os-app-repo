from django.db import models
from django.db.models import Sum, Avg, Min, Max, Count
from django.contrib.postgres.fields import JSONField
import json 
from pprint import pprint
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from .managers import DrugManager,PurchaseManager
from datetime import date, datetime



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
    name = models.CharField(max_length=100,primary_key=True)
    slug = models.SlugField()
    manufacturer= models.ForeignKey(Manufacturer, on_delete=models.CASCADE, to_field='name',related_name='drugs',blank=True, null=True)
    route_type= models.CharField(max_length=10,blank=True, null=True)
    cpt_dosage= models.CharField(max_length=100,blank=True, null=True)

    @property
    def meas_qty(self):
        return Contract.objects.get(drug_name=self.name).measured_equivalents_qty
    
    @property
    def meas_unit(self):
        return Contract.objects.get(drug_name=self.name).measured_equivalents_unit

    @property
    def all_purchases(self):
        if self.ndcs:
            r = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
            return r
        return []

    @property
    def q1(self):
        if self.ndcs:
            qtr_begin, qtr_end = (date(2019,1,1),date(2019,3,31))
            drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
            r = drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
            return r
        return []

    @property
    def q2(self):
        if self.ndcs:
            qtr_begin, qtr_end = (date(2019,4,1),date(2019,6,30))
            drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
            r =drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
            return r
        return []

    @property
    def q3(self):
        if self.ndcs:
            qtr_begin, qtr_end = (date(2019,7,1),date(2019,9,30))
            drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
            r = drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
            return r
        return []
    
    @property
    def q4(self):
        if self.ndcs:
            qtr_begin, qtr_end = (date(2019,10,1),date(2019,12,31))
            drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
            r = drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
            return r
        return []

    

    def contract_qty(self,qtr):
        meas_qty = Contract.objects.get(drug_name=self.name).measured_equivalents_qty
        meas_unit = Contract.objects.get(drug_name=self.name).measured_equivalents_unit

        if qtr == 1:
            qtr_begin, qtr_end = (date(2019,1,1),date(2019,3,31))
        elif qtr == 2:
            qtr_begin, qtr_end = (date(2019,4,1),date(2019,6,30))
        elif qtr == 3:
            qtr_begin, qtr_end = (date(2019,7,1),date(2019,9,30))
        else:
            qtr_begin, qtr_end = (date(2019,10,1),date(2019,12,31))

        
        drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
        r = drug_ps.filter(invoice_date__range=[qtr_begin, qtr_end])
        delivered_qty = r.aggregate(Sum('delivered_qty'))
        extended_delivered_qty = r.aggregate(Sum('extended_delivered_qty'))

        if r:
            if int(meas_qty) == 1 and meas_unit == 'BOTTLE':
                contract_qty = delivered_qty['delivered_qty__sum']
                return contract_qty
            else:
                contract_qty = extended_delivered_qty['extended_delivered_qty__sum'] / meas_qty
                return contract_qty
        else:
            contract_qty = None
            return contract_qty
        return contract_qty



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
    ndc_code= models.CharField(max_length=13,primary_key=True)
    hcpcs_code= models.CharField(max_length=5,blank=True, null=True)
    numerator_strength= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    cpt_mbu= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_package= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    package_qty= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_ndc= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    ndc_unit_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    @property
    def latest_claim(self):
        if self.purchases:
            latest_claim = self.purchases.all().latest()
            return latest_claim

    @property
    def latest_price(self):
        if self.purchases:
            latest_price = self.purchases.all().latest().unit_price
            return latest_price
    
    @property
    def latest_billing_unit_price(self):
        if self.purchases:
            latest_billing_unit_price = self.purchases.all().latest().billing_unit_price
            return latest_billing_unit_price

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
            self.contract_qty = Sum(self.delivered_qty)
            return self.contract_qty
        else:
            self.contract_qty = Sum(self.extended_delivered_qty) / self.measured_equivalents_qty
            return self.contract_qty

    def __str__(self):
        return f"Contract: {self.drug_name} Manufacturer: {self.manufacturer} Drug Category: {self.drug_category} Measured Equivalents: {self.measured_equivalents_qty}"



class Purchase(models.Model):

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        get_latest_by = ['invoice_date']

    os_account_id = models.CharField(max_length=6, blank=True, null=True)
    drug_name = models.CharField(max_length=100, blank=True, null=True)
    ndc_code = models.ForeignKey(NDC, on_delete=models.CASCADE, to_field='ndc_code', blank=True, null=True, related_name='purchases')
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
    
