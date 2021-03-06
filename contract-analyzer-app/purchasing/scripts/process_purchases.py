import csv
import pandas as pd
from datetime import datetime


def setPdOptions():
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', -1)

def addCreditColumn(delivered_qty):
    if delivered_qty < 0:
        return True
    else:
        return False

def formatColumns(input_df):
    formatted_columns = [
                'os_account_id', 'os_account', 'sales_order_id', 'customer_order_id', 'order_date', 'item_id',
                'item_description', 'os_ndc_code', 'unit_id', 'ordered_qty', 'delivered_qty',
                'backordered_qty', 'order_status', 'order_origin', 'unit_price', 'total_price',
                'total', 'lot_number', 'lot_expiration_date', 'invoice_number',
                'invoice_date', 'tracking_number', 'awp', 'os_hcpcs_code', 'billing_unit',
                'billint_unit_of_measure', 'contract_type', 'asp_per_billing_unit', 'manufacturer_id', 'os_parent_id',
                'is_refrigerated', 'billing_unit_price', 'billing_units_per_package',
                'forwarding_agent', 'item_schedule_code', 'item_group_code', 'item_group_code_description',
                'os_drug_name', 'therapeutic_first_subcategory_code_description', 'generic_name',
                'route_of_administration_code','route_of_administration_description'
        ]
    return formatted_columns

def convert_currency(currency_str):
    currency_str = str(currency_str).strip()
    try:
        if '(' in currency_str or ')' in currency_str:
            currency_num = float(str(currency_str).strip('(').strip(')').strip('$').replace(',', '')) * -1
        else:
            currency_num = float(str(currency_str).strip('(').strip(')').strip('$').replace(',', ''))
    except ValueError:
        currency_num = 0.0

    return currency_num

def preProcessData(input_df):
        df = input_df
        df.columns = formatColumns(input_df=input_df)
        df['is_credit'] = input_df['delivered_qty'].apply(lambda delivered_qty: addCreditColumn(delivered_qty))
        df['order_date'] = pd.to_datetime(input_df['order_date'])
        df['lot_expiration_date'] = pd.to_datetime(input_df['lot_expiration_date'])
        df['invoice_date'] = pd.to_datetime(input_df['invoice_date'], format='%Y%m%d')
        df['total'] = input_df['total'].apply(lambda total: convert_currency(total))
        df['total_price'] = input_df['total_price'].apply(lambda total: convert_currency(total))
        df['billing_unit_price'] = input_df['billing_unit_price'].apply(lambda billing_unit_price: convert_currency(billing_unit_price))
        df['unit_price'] = input_df['unit_price'].apply(lambda unit_price: convert_currency(unit_price))
        df['asp_per_billing_unit'] = input_df['asp_per_billing_unit'].apply(lambda asp_limit_per_bu: convert_currency(asp_limit_per_bu))
        df['awp'] = input_df['awp'].apply(lambda awp: convert_currency(awp))

        df = df.fillna(0)
        return df   

def mergeData(pre_processed_df):
    drugs_df = pd.read_csv('purchasing/models_data/ndcs.csv')
    merged_df = pd.merge(pre_processed_df,drugs_df,left_on='os_ndc_code',right_on='ndc_code')
    merged_df.columns = merged_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('#','number')
    merged_df['extended_ordered_qty'] = merged_df['ordered_qty'] * merged_df['ndc_unit_sum']
    merged_df['extended_delivered_qty'] = merged_df['delivered_qty'] * merged_df['ndc_unit_sum']
    return merged_df

def outputData(merged_df):
    output_df = pd.DataFrame(merged_df,columns =[
    'os_account_id',
    'drug_name',
    'ndc_code',
    'hcpcs_code',
    'order_date',
    'invoice_date',
    'item_description',
    'ordered_qty',
    'delivered_qty',
    'backordered_qty',
    'order_status',
    'unit_price',
    'total',
    'awp',
    'billing_unit',
    'billing_unit_price',
    'asp_per_billing_unit',
    'billing_units_per_package',
    'is_credit',
    'route_of_administration_code',
    'mbus_per_package',
    'ndc_unit_sum',
    'extended_ordered_qty',
    'extended_delivered_qty']
    )
    
    return output_df
    
def run():
    print(f'========================== PROCESSES_PURCHASES.PY ==========================')
    print(f'Setting PdOptions...')
    setPdOptions()

    print(f'Reading Recent Data...')
    recent_df = pd.read_excel('purchasing/purchase_data/preprocessed/recent_file.xlsx', index_col=0)
    
    print(f'Reading Data...')
    input_df = pd.read_excel('purchasing/purchase_data/preprocessed/preprocessed_combined_os_purchases.xlsx', index_col=0)
    
    print(f'Processing Data...')
    pre_processed_df = preProcessData(input_df=input_df)
    print(f'Merging Data...')
    merged_df = mergeData(pre_processed_df=pre_processed_df)
    print(f'Creating Output DataFrame...')
    output_df = outputData(merged_df=merged_df)

    # print(f'Writing Recent Output Data...')
    # output_df.to_excel('purchasing/purchase_data/processed/processed_recent_file.xlsx')

    print(f'Writing Output Data...')
    output_df.to_excel('purchasing/purchase_data/processed/processed_combined_recent_purchases.xlsx')
    print(f'Output Data Sample:')
    print(output_df.head())