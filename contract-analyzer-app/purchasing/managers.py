from django.db import models
from datetime import date, datetime

class DrugQuerySet(models.QuerySet):
    def get_orals(self):
        return self.filter(route_type__iexact='oral')
    def get_ivs(self):
        return self.filter(route_type__iexact='iv')

class DrugManager(models.Manager):
    def get_query_set(self):
        return DrugQuerySet(self.model, using=self._db)
    
    def get_orals(self):
        return self.get_query_set().get_orals()
    
    def get_ivs(self):
        return self.get_query_set().get_ivs()


class PurchaseQuerySet(models.QuerySet):
    def filter_by_drug(self,drug):
        return self.filter(drug_name__iexact=drug)

    def filter_by_date(self,q):
        if q == 1:
            qtr_begin, qtr_end = (date(2019,1,1),date(2019,3,31))
        elif q == 2:
            qtr_begin, qtr_end = (date(2019,4,1),date(2019,6,30))
        elif q == 3:
            qtr_begin, qtr_end = (date(2019,7,1),date(2019,9,30))
        else:
            qtr_begin, qtr_end = (date(2019,10,1),date(2019,12,31))
        return self.filter(invoice_date__range=[start,end])

class PurchaseManager(models.Manager):
    def get_query_set(self):
        return PurchaseQuerySet(self.model, using=self._db)
    
    def filter_by_date(self,q):
        return self.get_query_set().filter_by_date(q)
    
    def filter_by_drug(self,drug):
        return self.get_query_set().filter_by_drug(drug.name)

    
