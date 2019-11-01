import csv
import pandas as pd
from purchasing.models import Drug,Manufacturer,NDC,Contract,Purchase

def run():
    print(f'========================== LOAD_NDCS.PY ==========================')
    print(f'=========== START ===========')
    NDC.objects.all().delete()
    df = pd.read_csv('purchasing/models_data/ndcs.csv')
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')


    for idx,row in df.iterrows():
        n, created = NDC.objects.get_or_create(
        drug_name= Drug.objects.get(name__exact=row[0]),
        ndc_code=row[1],
        hcpcs_code=row[2],
        numerator_strength=row[3],
        cpt_mbu=row[4],
        mbus_per_package=row[5],
        package_qty=row[6],
        mbus_per_ndc=row[7],
        ndc_unit_sum=row[8]
        )
        n.save()
        print(f'{n.ndc_code} was added to database...')
    print('=================== DONE ===================')