import csv
import pandas as pd
from purchasing.models import Drug,Manufacturer,NDC,Contract,Purchase

def run():
    print(f'========================== LOAD_DRUGS.PY ==========================')
    print(f'=========== START ===========')
    Drug.objects.all().delete()
    df = pd.read_csv('purchasing/models_data/drugs.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        d, created = Drug.objects.get_or_create(
        name=row[0],
        manufacturer= Manufacturer.objects.get(name__exact=row[1]),
        route_type=row[2],
        cpt_dosage=row[3]
        )
        d.save()
        print(f'{d.name} was added to database...')
    print('=================== DONE ===================')