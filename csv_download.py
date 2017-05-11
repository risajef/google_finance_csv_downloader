import os
import urllib.request as urllib2
import datetime

# i = (Interval [minimum(60)]); p = (Samples); a day duration is 390min => 6.5h
GoogleFinancesLink = 'http://www.google.com/finance/getprices?i=60&p=390&f=d,o,h,l,c,v&df=cpct&q='

NASDAQ100 = ['FOXA', 'ATVI', 'ADBE', 'AKAM', 'ALXN', 'AMZN', 'AAL', 'AMGN', 'ADI', 'AAPL', 'AMAT', 'ADSK', 'ADP',
             'AVGO', 'BIDU', 'BBBY', 'BIIB', 'BMRN', 'CA', 'CELG', 'CERN', 'CHRW', 'CHTR', 'CHKP', 'CSCO', 'CTXS',
             'CTSH', 'CMCSA', 'COST', 'DISCA', 'DISH', 'DLTR', 'EBAY', 'EA', 'EQIX', 'EXPD', 'ESRX', 'FB', 'FAST',
             'FISV', 'GRMN', 'GILD', 'GOOG', 'HSIC', 'ILMN', 'INTC', 'INTU', 'ISRG', 'JD', 'KLAC', 'KHC', 'LRCX',
             'LBTYA', 'LVNTA', 'LMCA', 'LLTC', 'MAR', 'MAT', 'MU', 'MSFT', 'MDLZ', 'MNST', 'MYL', 'NTAP', 'NFLX',
             'NVDA', 'NXPI', 'ORLY', 'PCAR', 'PAYX', 'PCLN', 'QCOM', 'REGN', 'ROST', 'SNDK', 'SBAC', 'STX', 'SIRI',
             'SPLS', 'SBUX', 'SRCL', 'SYMC', 'TSLA', 'TXN', 'TSCO', 'TRIP', 'VRSK', 'VRTX', 'VIAB', 'VIP', 'VOD',
             'WDC', 'WFM', 'WYNN', 'XLNX', 'YHOO']
#  THESE DO NOT WORK: ALTR, BRCM, GMCR, SIAL

NYSE100 = ['JPM', 'VZ', 'KE', 'BABA', 'MRK', 'PG', 'CVX', 'SLB', 'WMT', 'V', 'HOT', 'MO', 'AIG', 'DIS',
           'MAR', 'CAT', 'BMY', 'DOW', 'MDT', 'AXP', 'LLY', 'TWX', 'VLO', 'RAI', 'LVS', 'HES', 'UAL', 'UNP', 'TGT',
           'PM', 'EOG', 'SO', 'CBS', 'GIS', 'LOW', 'TXN', 'MNK', 'EMR', 'OXY', 'UTX', 'MA', 'JAH', 'LYB', 'CRM', 'DD',
           'CNC', 'STT', 'DG', 'CL', 'ETN', 'MON', 'DE', 'RCL', 'DUK', 'KMX', 'COF', 'YUM', 'TSN', 'TJX', 'DHR',
           'D', 'PRU', 'JWN', 'VTR', 'HCA', 'FL', 'WM', 'CCI', 'NVS', 'AEP', 'TSO', 'PCG', 'PNC', 'FIS', 'ABC',
           'HP', 'HCN', 'MJN', 'IR', 'EW', 'STJ', 'AFL', 'VFC', 'ADI', 'EIX', 'NLSN', 'WSM', 'GPN', 'ALL', 'DRI', 'URI',
           'CPB', 'CAH', 'WEC', 'TIF', 'MSI', 'NSC']
#  THESE DO NOT WORK: OM, CAM, NIKE, UA
Stock_Names = ['NASDAQ', 'NYSE']
Stock_Data = [NASDAQ100, NYSE100]


# gets date and stores to "date"
def update_date():
    u = urllib2.urlopen(GoogleFinancesLink + 'AAPL')
    start = False
    date = ''
    for c in u.read(300):
        c = chr(c)
        if c == ',':
            start = False
        if start:
            date += c
        if c == 'a':
            start = True
    date = int(date)  # cast to int
    date = datetime.datetime.fromtimestamp(date)  # cast do readable date
    date = date.strftime('%Y/%m/%d')  # cast to String of Format 2016/12/31
    year = ''
    month = ''
    day = ''
    for i, y in enumerate(date):
        if i < 4:
            year = year + y
        elif 4 < i & i < 7:
            month = month + y
        elif 7 < i:
            day = day + y
    return year, month, day


def download_data():
    [year, month, day] = update_date()
    for i, e in enumerate(Stock_Data):
        if not os.path.exists(Stock_Names[i]):
            os.makedirs(Stock_Names[i])
        os.chdir(Stock_Names[i])
        if not os.path.exists(month):
            os.makedirs(month)
        os.chdir(month)
        for j, s in enumerate(e):
            Stock_Data[i][j] = GoogleFinancesLink + s
            u = urllib2.urlopen(Stock_Data[i][j])
            localFile = open(day + '_' + s + '.csv', 'wb')
            localFile.write(u.read())
            localFile.close()
        os.chdir('../../')
    return


def clean_up():
    os.chdir('../')
    for (path, dirs, files) in os.walk(year):
        for f in files:
            localFile = open(str(path) + '/' + str(f))
            if os.path.getsize(localFile.name) < 1000:
                print(str(localFile.name) + ' : ' + str(os.path.getsize(localFile.name)))
                localFile.close()
                os.remove(localFile.name)
            else:
                localFile.close()


# main function
if not os.path.exists('STOCKS'):
    os.makedirs('STOCKS')
[year, month, day] = update_date()
if not os.path.exists(year):
    os.makedirs(year)
os.chdir(year)
download_data()
clean_up()
