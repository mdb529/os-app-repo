from django.db import models
from django.contrib.postgres.fields import JSONField
import json 
from pprint import pprint
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify


class Manufacturer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    logo_img= models.ImageField(upload_to="logos/",blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Drug(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
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
        unique_together = ('ndc_code', 'hcpcs_code')

    name = models.ForeignKey(Drug, on_delete=models.CASCADE, to_field='name', related_name='ndcs')
    ndc_code= models.CharField(max_length=13)
    hcpcs_code= models.CharField(max_length=5,blank=True, null=True)
    numerator_strength= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    cpt_mbu= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_package= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    package_qty= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_ndc= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    units_of_service = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.ndc_code} | {self.numerator_strength}"
    
# class Contract(models.Model):

#     CONTRACT_TYPES = (
#         ('G','Growth'),
#         ('V','Volume'),
#         ('VG','Volume And Growth'),
#         ('MS','Market Share'),
#         ('P','Portfolio')
#     )
    

#     drug_name= models.ForeignKey(Drug, on_delete=models.CASCADE, null=True, related_name="contracted_drugs")
#     type= models.CharField(choices=CONTRACT_TYPES, max_length=50)
#     drug_category= models.CharField(max_length=10, blank=True, null=True)
#     date= models.DateField(blank=True, null=True)
#     equivalent_measure= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
#     baseline_start_date= models.DateField(blank=True, null=True)
#     baseline_end_date= models.DateField(blank=True, null=True)
#     baseline_measure= models.CharField(max_length=50, blank=True, null=True)
#     rebate_schedule= JSONField(blank=True, null=True)


#     def __str__(self):
#         return f"Contract Drug Type: {self.drug_category} Contract Type: {self.type} Date: {self.contract_date} Contract Drug: {self.contract_drug_name} Contract Manufacturer: {self.contract_manufacturer}"