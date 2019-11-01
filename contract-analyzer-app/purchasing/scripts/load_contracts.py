import csv
import pandas as pd
from purchasing.models import Drug,Manufacturer,NDC,Contract

def run():

    
    Contract.objects.all().delete()
    df = pd.read_csv('purchasing/models_data/contracts.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        c, created = Contract.objects.get_or_create(
        drug_name= Drug.objects.get(name__exact=row[0]),
        manufacturer= Manufacturer.objects.get(name__exact=row[1]),
        drug_category=row[2],
        measured_equivalents_qty=row[3],
        measured_equivalents_unit=row[4],
        effective_start_date=row[5],
        effective_end_date=row[6],
        )
        c.save()
        print(f'{c} was added to database...')
    
    print('=================== DONE ===================')