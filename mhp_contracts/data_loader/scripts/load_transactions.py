import csv
import pandas as pd
from data_loader.models import Transaction
from os_contracts.models import Drug,NDC,Manufacturer


def wipe_transactions():
    print(f'Deleting objects from Transaction table...')
    Transaction.objects.all().delete()

def load_historical_transactions():
    print(f'========================== LOAD_HISTORICAL_TRANSACTIONS.PY ==========================')

    df1 = pd.read_excel('data_loader/processed_purchase_data/historical_os_purchases.xlsx',index_col=0)
    df1 = df1.fillna(0)
    df1.columns = df1.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')

    print('Loading Historical Purchases...')
    for idx, row in df1.iterrows():
        t, created = Transaction.objects.get_or_create(
        os_account_id=row[0],
        drug_name = row[1],        
        ndc_code = NDC.objects.get(ndc_code__exact=row[2]),
        hcpcs_code = row[3],
        order_date = row[4],
        invoice_date = row[5],
        item_description = row[6],
        ordered_qty = row[7],
        delivered_qty = row[8],
        backordered_qty = row[9],
        order_status = row[10],
        unit_price = row[11],
        total = row[12],
        awp = row[13],
        billing_unit = row[14],
        billing_unit_price=row[15],
        asp_per_billing_unit = row[16],
        billing_units_per_package = row[17],
        is_credit = row[18],
        route_of_administration_description = row[19],
        mbus_per_ndc = row[20],
        ndc_unit_sum = row[21],
        extended_ordered_qty = row[22],
        extended_delivered_qty=row[23],
        )
        t.save()
        print(f'{t} was added to database...')
    print('\n')     
    print('...Historical Purchases Successfully Loaded')
    print('\n')

def load_recent_transactions():
    print(f'========================== LOAD_RECENT_TRANSACTIONS.PY ==========================')

    df2 = pd.read_excel('data_loader/processed_purchase_data/processed_recent_purchases.xlsx',index_col=0)
    df2 = df2.fillna(0)
    df2.columns = df2.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')','').str.replace('#', 'number')

    print('Loading Recent Purchases...')
    for idx, row in df2.iterrows():
        t, created = Transaction.objects.get_or_create(
        os_account_id = row[0],
        drug_name = row[1],   
        ndc_code = NDC.objects.get(ndc_code__exact=row[2]),
        hcpcs_code = row[3],
        order_date = row[4],
        invoice_date = row[5],
        item_description = row[6],
        ordered_qty = row[7],
        delivered_qty = row[8],
        backordered_qty = row[9],
        order_status = row[10],
        unit_price = row[11],
        total = row[12],
        awp = row[13],
        billing_unit = row[14],
        billing_unit_price=row[15],
        asp_per_billing_unit = row[16],
        billing_units_per_package = row[17],
        is_credit = row[18],
        route_of_administration_description = row[19],
        mbus_per_ndc = row[20],
        ndc_unit_sum = row[21],
        extended_ordered_qty = row[22],
        extended_delivered_qty = row[23],
        )
        t.save()
        print(f'{t} was added to database...')
    
    print('\n')
    print('...Recent Purchases Successfully Loaded')

def run():
    print('============= START =============')
    print('\n')
    wipe_transactions()
    load_historical_transactions()
    load_recent_transactions()
    print('\n')
    print('============= DONE =============')