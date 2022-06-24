start_year = 2021
start_month = 12
start_day = 31

end_year = 2022
end_month = 1
end_day = 1

units = ["LARYO-2", "LNCSO-2"] # NGC BM Unit ID












import requests
import csv
import datetime
import smtplib
import time
import email
from email.mime.text import MIMEText


apikey = "e7dnu62uyibzbyb" # apikey
servicetype = "CSV" # CSV / XML

all_dates = []

apibase= "https://api.bmreports.com/BMRS/B1610/<VersionNo>? APIKey =< APIKey>&SettlementDate=<SettlementDate>&Period=<Period>&NGCBMUnitID=<NGCBMUnitID>&ServiceType=<xml/XML/csv/CSV>"

apiexample = "https://api.bmreports.com/BMRS/B1610/v2? APIKey=e7dnu62uyibzbyb&SettlementDate=2021-12-31&Period=48&NGCBMUnitID=LNCSO-1&ServiceType=CSV"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

start_date = datetime.date(start_year, start_month, start_day)
end_date = datetime.date(end_year, end_month, end_day)
for single_date in daterange(start_date, end_date):
    all_dates.append(single_date.strftime("%Y-%m-%d"))


for unit in units:
    fin = open(f"{unit} {start_year}-{start_month}-{start_day}.txt", "a+")

    for j in range(len(all_dates)):
      day = all_dates[j]
      for i in range(1,49):
        apifstring = f"https://api.bmreports.com/BMRS/B1610/v2? APIKey={apikey}&SettlementDate={day}&Period={i}&NGCBMUnitID={unit}&ServiceType={servicetype}"

        with requests.get(apifstring) as r:
          lines = (line.decode('utf-8') for line in r.iter_lines())
          for row in csv.reader(lines):
            try:
              infotoget = (row[10])
            except KeyError:
              print(f"Data does not exist for date: {day} period: {i}")
              infotoget = "0"
              pass
            except:
              infotoget = "0"
              pass

        print(day + " " + str(i) + " " + infotoget)
        fin.write(day + " " + str(i) + " " + infotoget+"\n")

    fin.close()    
    # email sending when done


    ################# SMTP SSL ################################
    start = time.time()
    try:
        smtp_ssl = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
    except Exception as e:
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
        smtp_ssl = None

    print("Connection Object : {}".format(smtp_ssl))
    print("Total Time Taken  : {:,.2f} Seconds".format(time.time() - start))

    ######### Log In to mail account ############################
    print("\nLogging In.....")
    resp_code, response = smtp_ssl.login(user="hicks.harryj@gmail.com", password="ztczmbxiuxzlsjen")

    print("Response Code : {}".format(resp_code))
    print("Response      : {}".format(response.decode()))

    ################ Send Mail ########################
    print("\nSending Mail..........")

    message = email.message.EmailMessage()
    message.set_default_type("text/plain")

    frm = "hicks.harryj@gmail.com"
    to_list = ["matthew.hicks@inchoo.org.uk"]
    message["From"] = frm
    message["To"] = to_list
    message["Subject"] =  "Finished File"

    body = f'''
    File finished generating for {unit} {start_year}-{start_month}-{start_day}. See attached.
    '''
    message.set_content(body)

    txtfile = f"{unit} {start_year}-{start_month}-{start_day}.txt"

    with open(txtfile, "rb") as f:
        file_data = f.read()
        file_name = f.name

    message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=txtfile)

    response = smtp_ssl.sendmail(from_addr=frm,
                                 to_addrs=to_list,
                                 msg=message.as_string())

    print("\nLogging Out....")
    resp_code, response = smtp_ssl.quit()

    print("Response Code : {}".format(resp_code))
    print("Response      : {}".format(response.decode()))




# ['Actual Generation Output Per Generation Unit (B1610)']
# ['Time Series ID', 'Registered Resource  EIC Code', 'BM Unit ID', 'NGC BM Unit ID', 'PSR Type', 'Market Generation Unit EIC Code', 'Market Generation BMU ID', 'Market Generation NGC BM Unit ID', 'Settlement Date', 'SP', 'Quantity (MW)']
# ['ELX-EMFIP-AGOG-TS-22849', '48W00000LNCSO-1R', 'T_LNCSW-1', 'LNCSO-1', 'Generation', '48W00000LNCSO-1R', 'T_LNCSW-1', 'LNCSO-1', '2021-12-31', '48', '119.362']
