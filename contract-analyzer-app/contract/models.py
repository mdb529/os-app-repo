from django.db import models
from purchasing.models import Manufacturer,Drug,NDC,Purchase


class BaseIncentive(models.Model):
    class Meta:
        abstract = True


    
class BaseCondition(models.Model):
    class Meta:
        abstract = True



class BaseContract(models.Model):
    class Meta:
        abstract = True






# class Contract(models.Model):
#     class Meta:
#         ordering = ['drug_name']

#     CONTRACT_TYPES = (
#         ('G','Growth'),
#         ('V','Volume'),
#         ('MS','Market Share'),
#         ('P', 'Portfolio'),
#         ('VG','Volume/Growth'),
#         ('GMS', 'Growth/Market Share'),
#         ('GP', 'Growth/Portfolio'),
#         ('VMS', 'Volume/Market Share'),
#         ('VMS', 'Volume/Market Share'),
#     )

#     drug_name= models.OneToOneField(Drug, on_delete=models.CASCADE, to_field='name')
#     manufacturer= models.ForeignKey(Manufacturer, on_delete=models.CASCADE, to_field='name',related_name='contracts')
#     drug_category= models.CharField(max_length=10, blank=True, null=True)
#     measured_equivalents_qty= models.DecimalField(max_digits=15,decimal_places=4,blank=True, null=True)
#     measured_equivalents_unit= models.CharField(max_length=10, blank=True, null=True)
#     contract_type= models.CharField(choices=CONTRACT_TYPES, max_length=50,blank=True, null=True)
#     effective_start_date= models.DateField(blank=True, null=True)
#     effective_end_date = models.DateField(blank=True, null=True)
#     measurement_period_start_date= models.DateField(blank=True, null=True)
#     measurement_period_end_date = models.DateField(blank=True, null=True)
#     baseline = models.DecimalField(max_digits=15,decimal_places=4,blank=True, null=True)
#     baseline_start_date= models.DateField(blank=True, null=True)
#     baseline_end_date= models.DateField(blank=True, null=True)
#     baseline_measure= models.CharField(max_length=50, blank=True, null=True)
#     rebate_schedule = JSONField(blank=True, null=True)
#     discount_schedule = JSONField(blank=True, null=True)
    
    # @property
    # def meas_qty(self):
    #     return Contract.objects.get(drug_name=self.name).measured_equivalents_qty
    
    # @property
    # def meas_unit(self):
    #     return Contract.objects.get(drug_name=self.name).measured_equivalents_unit

    # @property
    # def all_purchases(self):
    #     if self.ndcs:
    #         r = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
    #         return r
    #     return []

    # @property
    # def q1(self):
    #     if self.ndcs:
    #         qtr_begin, qtr_end = (date(2019,1,1),date(2019,3,31))
    #         drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
    #         r = drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
    #         return r
    #     return []

    # @property
    # def q2(self):
    #     if self.ndcs:
    #         qtr_begin, qtr_end = (date(2019,4,1),date(2019,6,30))
    #         drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
    #         r =drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
    #         return r
    #     return []

    # @property
    # def q3(self):
    #     if self.ndcs:
    #         qtr_begin, qtr_end = (date(2019,7,1),date(2019,9,30))
    #         drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
    #         r = drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
    #         return r
    #     return []
    
    # @property
    # def q4(self):
    #     if self.ndcs:
    #         qtr_begin, qtr_end = (date(2019,10,1),date(2019,12,31))
    #         drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
    #         r = drug_ps.filter(invoice_date__range=[qtr_begin,qtr_end])
    #         return r
    #     return []
    

    # def contract_qty(self,qtr):
        # meas_qty = Contract.objects.get(drug_name=self.name).measured_equivalents_qty
        # meas_unit = Contract.objects.get(drug_name=self.name).measured_equivalents_unit

        # if qtr == 1:
        #     qtr_begin, qtr_end = (date(2019,1,1),date(2019,3,31))
        # elif qtr == 2:
        #     qtr_begin, qtr_end = (date(2019,4,1),date(2019,6,30))
        # elif qtr == 3:
        #     qtr_begin, qtr_end = (date(2019,7,1),date(2019,9,30))
        # else:
        #     qtr_begin, qtr_end = (date(2019,10,1),date(2019,12,31))

        
        # drug_ps = Purchase.objects.filter(ndc_code__in=self.ndcs.all())
        # r = drug_ps.filter(invoice_date__range=[qtr_begin, qtr_end])
        # delivered_qty = r.aggregate(Sum('delivered_qty'))
        # extended_delivered_qty = r.aggregate(Sum('extended_delivered_qty'))

        # if r:
        #     if int(meas_qty) == 1 and meas_unit == 'BOTTLE':
        #         contract_qty = delivered_qty['delivered_qty__sum']
        #         return contract_qty
        #     else:
        #         contract_qty = Decimal(extended_delivered_qty['extended_delivered_qty__sum']) / Decimal(meas_qty)
        #         return contract_qty
        # else:
        #     contract_qty = None
        #     return contract_qty
            
        # return contract_qty


#     def __str__(self):
#         return f"{self.drug_name}"