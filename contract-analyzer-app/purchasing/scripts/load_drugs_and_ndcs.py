import csv
import pandas as pd
from purchasing.models import Drug,Manufacturer,NDC,Contract,Purchase

def run():
    print(f'========================== LOAD_DRUGS_AND_NDCS.PY ==========================')
    print(f'=========== START ===========')
    NDC.objects.all().delete()
    df = pd.read_csv('purchasing/models_data/drugs_and_ndcs.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        n, created = NDC.objects.get_or_create(
        name= row[0],
        manufacturer= Manufacturer.objects.get(name__exact=row[1]),
        route_type=row[2],
        cpt_dosage=row[3],
        ndc_code=row[4],
        hcpcs_code=row[5],
        numerator_strength=row[6],
        cpt_mbu=row[7],
        mbus_per_package=row[8],
        package_qty=row[9],
        mbus_per_ndc=row[10],
        ndc_unit_sum=row[11]
        )
        n.save()
        print(f'{n.ndc_code} was added to database...')
        print(f'=========== END ===========')