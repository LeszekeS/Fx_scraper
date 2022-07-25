import requests
from bs4 import BeautifulSoup
import datetime
from openpyxl import Workbook

def rates_cz(code, startY, startM, startD, endY, endM, endD):

    startDate = f"{startD}.{startM}.{startY}"
    endDate = f"{endD}.{endM}.{endY}"

    resp = requests.get(f"https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/selected.txt?from={startDate}&to={endDate}&currency={code}&format=txt")

    resp = BeautifulSoup(resp.content, "html.parser")
    resp = BeautifulSoup.get_text(resp)
    resp = resp.split("\n")

    rates = {}
    first_date = ""
    for i, value in enumerate(resp):
        if i > 1 and len(value.split("|")) == 2:
            date = value.split("|")[0].split(".")
            rate = value.split("|")[1]
            rates[f"{date[2]}-{date[1]}-{date[0]}"] = rate
        if i == 2:
            first_date = value.split("|")[0].split(".")
            first_date = f"{first_date[2]}-{first_date[1]}-{first_date[0]}"

    return [rates, code, first_date]


def rates_pl(code, startY, startM, startD, endY, endM, endD):

    start_date = f"{startY}-{startM}-{startD}"
    end_date = f"{endY}-{endM}-{endD}"

    res = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/{start_date}/{end_date}/?format=json")

    resp = res.json()

    rates = {}
    first_date = ""
    for i, value in enumerate(resp["rates"]):
        rates[value['effectiveDate']] = value['mid']
        if i == 0:
            first_date = value['effectiveDate']

    return [rates, code, first_date]

def rates_hr(code, startY, startM, startD, endY, endM, endD):

    start_date = f"{startY}-{startM}-{startD}"
    end_date = f"{endY}-{endM}-{endD}"

    res = requests.get(f"https://api.hnb.hr/tecajn/v1?valuta={code}&datum-od={start_date}&datum-do={end_date}")
    resp = res.json()

    rates = {}


    first_date = ""
    for i, value in enumerate(resp):
        date = value["Datum primjene"].split(".")
        date = f"{date[2]}-{date[1]}-{date[0]}"
        rates[date] = value["Srednji za devize"].replace(",",".")
        if i == 0:
            first_date = value["Datum primjene"].split(".")
            first_date = f"{first_date[2]}-{first_date[1]}-{first_date[0]}"

    return [rates, code, first_date]

def rates_bg(code, startY, startM, startD, endY, endM, endD):

    resp = requests.get(f"https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?downloadOper=&group1=second&periodStartDays={startD}&periodStartMonths={startM}&periodStartYear={startY}&periodEndDays={endD}&periodEndMonths={endM}&periodEndYear={endY}&valutes={code}&search=true&showChart=false&showChartButton=true")
    resp = BeautifulSoup(resp.content, "html.parser")
    resp = resp.find("div", {'class':'table_box table_scroll'})
    resp = resp.find_all("td")

    table = []
    row = []
    first_date = ""
    for i, value in enumerate(resp):
        if value["class"] == ['first', 'center']:
            date = BeautifulSoup.get_text(value).split(".")
            row.append(f"{date[2]}-{date[1]}-{date[0]}")
            if i == 0:
                first_date = f"{date[2]}-{date[1]}-{date[0]}"
        if value["class"] == ['center']:
            quant = int(BeautifulSoup.get_text(value))
            row.append(quant)
        if value["class"] == ['last', 'center']:
            rate = float(BeautifulSoup.get_text(value))
            row.append(rate)
            table.append(row)
            row = []

    rates = {}

    for i in table:
        rates[i[0]] = i[2]/i[1]

    return [rates, code, first_date]


def xl_input(rates, endY, endM, endD):

    first_date = rates[2].split("-")
    date = datetime.date(int(first_date[0]), int(first_date[1]), int(first_date[2]))
    end_date = datetime.date(int(endY), int(endM), int(endD))
    delta = datetime.timedelta(days=1)

    i = 0
    xl_list = []

    while date <= end_date:
        if date.strftime("%Y-%m-%d") in rates[0]:
            rate = float(rates[0][date.strftime("%Y-%m-%d")])
        else:
            rate = float(xl_list[i - 1][2])

        xl_list.append([rates[1], (date - datetime.date(1900,1,1)).days + 2, rate])

        date += delta

    return xl_list


def create_file(data, file_name):

    wb = Workbook()
    ws = wb["Sheet"]
    ws.title = "Rates"

    ws.append(["Currency", "Valid On", "Rate Value"])
    for i, value in enumerate(data):
        ws.append(value)
        ws[f"B{i+2}"].number_format = 'dd-mm-yyyy'

    wb.save(f"Exchange rates - Data import template_{file_name}.xlsx")

def last_day(year, month):
    days = {"01":"31", "02":"28", "03":"31", "04":"30", "05":"31", "06":"30",
            "07":"31", "08":"31", "09":"30", "10":"31", "11":"30", "12":"31",}

    if int(year) % 4 == 0 and month == "02":
        day = "29"
    else:
        day = days[month]

    return day

