from django.db import models
from django.contrib.postgres.fields import JSONField
import json 
from pprint import pprint
from django.core.files.storage import FileSystemStorage


class Manufacturer(models.Model):
    name= models.CharField(max_length=50,unique=True)
    logo_img= models.ImageField(upload_to="logos/",blank=True,null=True)

    def __str__(self):
        return f"{self.name}"


class Drug(models.Model):
    class Meta:
        unique_together = ('ndc_code', 'hcpcs_code')

    ndc_code= models.CharField(max_length=13)
    name= models.CharField(max_length=100)
    hcpcs_code= models.CharField(max_length=5,blank=True, null=True)
    manufacturer= models.ForeignKey(Manufacturer, on_delete=models.CASCADE, to_field='name',related_name='drugs')
    route_type= models.CharField(max_length=10,blank=True, null=True)
    cpt_dosage= models.CharField(max_length=100,blank=True, null=True)
    numerator_strength= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    cpt_mbu= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_package= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    package_qty= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    mbus_per_ndc= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    units_of_service= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)


    def __str__(self):
        return f"{self.name}"



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