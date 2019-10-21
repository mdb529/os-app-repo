import csv
import pandas as pd
from os_contracts.models import Drug,Manufacturer

def run():

    
    Drug.objects.all().delete()
    df = pd.read_csv('os_contracts/temp/drugs.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        d, created = Drug.objects.get_or_create(
        name=row[0],
        ndc_code=row[1],
        hcpcs_code=row[2],
        manufacturer= Manufacturer.objects.get(manufacturer__exact=row[3]),
        route_type=row[4],
        cpt_dosage=row[5],
        numerator_strength=row[6],
        cpt_mbu=row[7],
        mbus_per_package=row[8],
        package_qty=row[9],
        mbus_per_ndc=row[10],
        units_of_service=row[11]
        )
        d.save()
        print(f'{d.name} was added to database...')