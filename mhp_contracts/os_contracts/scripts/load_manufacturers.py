import csv
import pandas as pd
from os_contracts.models import Drug,Manufacturer

def run():

    Manufacturer.objects.all().delete()
    df = pd.read_csv('os_contracts/temp/manufacturers.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        m, created = Manufacturer.objects.get_or_create(
        name=row[0]
        )
        m.save()
        print(f'{m.name} was added to database...')