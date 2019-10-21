import csv
import pandas as pd
from os_contracts.models import Drug,Manufacturer,NDC

def run():

    
    NDC.objects.all().delete()
    df = pd.read_csv('os_contracts/temp/ndcs.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        n, created = NDC.objects.get_or_create(
        name= Drug.objects.get(name__exact=row[0]),
        ndc_code=row[1],
        hcpcs_code=row[2],
        numerator_strength=row[3],
        cpt_mbu=row[4],
        mbus_per_package=row[5],
        package_qty=row[6],
        mbus_per_ndc=row[7],
        units_of_service=row[8]
        )
        n.save()
        print(f'{n.ndc_code} was added to database...')