import csv
import sys

dick = sys.argv[1]

with open(dick, newline='', encoding='big5') as csvfile:
    rows = csv.DictReader(csvfile)

    months = []
    for row in rows:
        if row['商品代號'] == 'TX     ':
            month = row['到期月份(週別)'].replace(' ', '')
            if len(month) <= 6:
                months.append(int(month))
    min_month = min(months)
    # print('min_month = {}'.format(min_month))

with open(dick, newline='', encoding='big5') as csvfile:
    rows = csv.DictReader(csvfile)

    # count = 0
    TX_all = []
    for row in rows:
        if row['商品代號'] == 'TX     ':
            date = int(row['成交日期'].replace(' ', ''))
            month = row['到期月份(週別)'].replace(' ', '')
            time = int(row['成交時間'].replace(' ', ''))
            price = float(row['成交價格'].replace(' ', ''))
            if len(month) <= 6:
                if int(month) == min_month and time >= 84500 and time <= 134500:
                    TX_all.append((date, time, price))
        
o = int(TX_all[0][2])
c = int(TX_all[-1][2])
all_prices = [k[2] for k in TX_all]
h = int(max(all_prices))
l = int(min(all_prices))
print(o, h, l, c)