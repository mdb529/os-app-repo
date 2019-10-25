import csv
import pandas as pd
from data_loader.models import Transaction
from os_contracts.models import Drug,NDC,Manufacturer

def run():

    
    Transaction.objects.all().delete()
    df = pd.read_excel('data_loader/processed_purchase_data/OS Purchases.xlsx',index_col=0)
    df = df.fillna(0)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')



    for idx, row in df.iterrows():
        t, created = Transaction.objects.get_or_create(
        os_account_id = row[0],
        os_account = row[1],
        drug_name = row[2],
        ndc_code = row[3],
        hcpcs_code = row[4],
        order_date = row[5],
        invoice_date = row[6],
        item_description = row[7],
        ordered_quantity = row[8],
        delivered_quantity = row[9],
        backordered_quantity = row[10],
        order_status = row[11],
        unit_price = row[12],
        total = row[13],
        awp = row[14],
        billing_unit = row[15],
        billing_unit_price = row[16],
        billing_units_per_package = row[17],
        asp_per_billing_unit = row[18],
        is_credit = row[19],
        route_of_administration_code_description = row[20],
        mbus_per_ndc = row[21],
        units_of_service = row[22],
        extended_ordered_qty = row[23],
        extended_delivered_qty = row[24],
        )
        t.save()
        print(f'{t} was added to database...')
    
    print('DONE')