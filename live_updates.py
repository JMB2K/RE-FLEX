import time
from datetime import date

try:
    import userdata.serviceAreaIds as serviceAreaIds
except:
    pass



def live_mode(block):
    block_length = (block['endTime'] - block['startTime']) / 3600
    block_price = block['rateInfo']['priceAmount']
    block_headstart = block['startTime'] - int(time.time())
    block_rate = block_price / block_length
    try:
        print('----------------------------------')
        print('Scanned at', time.strftime('%m/%d/%Y %I:%M:%S %p'))
        print('----------------------------------')
        if block['offerType'] == 'EXCLUSIVE': print('* * R E S E R V E D * *')
        print(date.fromtimestamp(block['startTime']).strftime('%A'), time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime'])))
        print('Starts in:')
        if round((block_headstart) / 60, 2) < 60: print(round((block_headstart) / 60, 2), 'minutes')
        if 1 < round((block_headstart) / 3600, 2) < 24: print(round((block_headstart) / 3600, 2), 'hours')
        if 1 < round(((block_headstart) / 3600) / 24, 2): print(round(((block_headstart) / 3600) / 24, 2), 'days')
        print(serviceAreaIds.stationlist[block['serviceAreaId']])
        print(round(block_length, 1), 'Hours')
        print(round(block_price, 2), 'Dollars')
        print(round(block_rate, 2), '/hr')
        if block['offerType'] == 'EXCLUSIVE': print('* * R E S E R V E D * *')
        print('----------------------------------')
    except KeyError:
        print('live mode glitch')

def live_rapid(block):
    block_length = (block['endTime'] - block['startTime']) / 3600
    block_price = block['rateInfo']['priceAmount']
    block_rate = block_price / block_length
    try:
        print('----------------------------------')
        print('Trying again', time.strftime('%m/%d/%Y %I:%M:%S %p'))
        print('----------------------------------')
        print(serviceAreaIds.stationlist[block['serviceAreaId']])
        print(round(block_length, 1), 'Hours')
        print(round(block_rate, 2), '/hr')
        print('----------------------------------')
    except KeyError:
        print('live rapid glitch')

def print_history(block):
    block_length = (block['endTime'] - block['startTime']) / 3600
    block_price = block['rateInfo']['priceAmount']
    block_rate = block_price / block_length
    try:
        with open('scandata/scanned_blocks', 'a') as f:
            print('----------------------------------', file=f)
            print('Scanned at', time.strftime('%m/%d/%Y %I:%M:%S %p'), file=f)
            print('----------------------------------', file=f)
            if block['offerType'] == 'EXCLUSIVE': print('* * R E S E R V E D * *', file=f)
            print(date.fromtimestamp(block['startTime']).strftime('%A'), time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime'])), file=f)
            print(serviceAreaIds.stationlist[block['serviceAreaId']], file=f)
            print(round(block_length, 1), 'Hours', file=f)
            print(round(block_price, 1), 'Dollars', file=f)
            print(round(block_rate, 2), '/hr', file=f)
            if block['offerType'] == 'EXCLUSIVE': print('* * R E S E R V E D * *', file=f)
            print('----------------------------------', file=f)
    except KeyError:
        print('print history glitch')


def rapid_history(block):
    block_length = (block['endTime'] - block['startTime']) / 3600
    block_price = block['rateInfo']['priceAmount']
    block_rate = block_price / block_length
    try:
        with open('scandata/scanned_blocks', 'a') as f:
            print('----------------------------------', file=f)
            print('Again at', time.strftime('%m/%d/%Y %I:%M:%S %p'), file=f)
            print('----------------------------------', file=f)
            print(serviceAreaIds.stationlist[block['serviceAreaId']], file=f)
            print(round(block_length, 1), 'Hours', file=f)
            print(round(block_rate, 2), '/hr', file=f)
            print('----------------------------------', file=f)
    except KeyError:
        print('print history glitch')
