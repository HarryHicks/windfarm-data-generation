start_year = 2019
start_month = 1
start_day = 1

end_year = 2020
end_month = 1
end_day = 1

unit = "LNCSO-1" # NGC BM Unit ID












import requests
import csv
import datetime


apikey = "" # apikey.               API KEY HERE
date = "2021-12-31" # YYYY-MM-DD
period = "48" # between 0 and 48 (every 30 mins)
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
    fin = open("data.txt", "a+")
    fin.write(day + " " + str(i) + " " + infotoget+"\n")
    fin.close()
    
# ['Actual Generation Output Per Generation Unit (B1610)']
# ['Time Series ID', 'Registered Resource  EIC Code', 'BM Unit ID', 'NGC BM Unit ID', 'PSR Type', 'Market Generation Unit EIC Code', 'Market Generation BMU ID', 'Market Generation NGC BM Unit ID', 'Settlement Date', 'SP', 'Quantity (MW)']
# ['ELX-EMFIP-AGOG-TS-22849', '48W00000LNCSO-1R', 'T_LNCSW-1', 'LNCSO-1', 'Generation', '48W00000LNCSO-1R', 'T_LNCSW-1', 'LNCSO-1', '2021-12-31', '48', '119.362']
