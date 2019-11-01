import imaplib
import base64
import os, glob
import email
from datetime import datetime, timedelta
import xlrd
import xlwt
import pandas as pd

u = 'mdb529@gmail.com'
p = 'wlevorefihfhlzoc'

today = datetime.now()
yesterday = today - timedelta(days=1)

def retrieveEmail():
    email_user = u
    email_pass = p

    mail = imaplib.IMAP4_SSL('imap.gmail.com','993')
    mail.login(email_user, email_pass)
    print(f'Logged in')
    mail.select('INBOX')

    type, data = mail.search(None, 'SUBJECT "MHP Purchase Detail"')
    mail_ids = data[0]
    id_list=mail_ids.split()

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        email_date = email_message['Date']
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        received_date = datetime(year=int(date_tuple[0]),month=int(date_tuple[1]),day=int(date_tuple[2]))


        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            email_attachment_name = part.get_filename()
            if bool(email_attachment_name):
                fileName = 'os_purchases_{0}.xls'.format(received_date.strftime("%Y%m%d"))
                filePath = os.path.join('purchasing/purchase_data/raw/', fileName)
                if not os.path.isfile(filePath):
                    xlfile = open(filePath, 'wb')
                    xlfile.write(part.get_payload(decode=True))
                    xlfile.close()
                print(f'Downloaded "{fileName}"')

def loadData():
    app_fp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    fp = os.path.join(app_fp, 'purchase_data/raw/*')
    file_list = glob.glob(fp)
    output_file_name = 'preprocessed_os_purchases.xlsx'
    output_fp = os.path.join(app_fp, 'purchase_data/preprocessed/{0}'.format(output_file_name))

    appended_data = []

    for in_file in file_list:
        print(f'Reading file {in_file}...')
        df = pd.read_excel(in_file)
        print(f'Appending data...')
        appended_data.append(df)
    print(f'-- combining recent purchase data ---')
    appended_data_df = pd.concat(appended_data)
    print(f'writing file "{output_file_name}"...')
    appended_data_df.to_excel(output_fp)
    print(f'================== UPLOAD SUCCESSFUL! ==================')



def run():
    print(f'========================== LOAD_DATA.PY ==========================')
    print(f'------------------ retrieveEmail() ------------------')
    retrieveEmail()
    print(f'------------------ processData() ------------------')
    loadData()
    print('=================== DONE ===================')
