import time
from datetime import date

try:
    import userdata.serviceAreaIds as serviceAreaIds
except:
    pass

def scan_print(block):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_rate = block_price / block_length
    try:
        with open ("scandata/recent-scans", "a") as r:
            print(serviceAreaIds.stationlist[block['serviceAreaId']], file=r)
            print(date.fromtimestamp(block['startTime']).strftime('%A'), time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime'])), file=r)
            print(round(block_length, 1), 'Hours', file=r)
            print('$',block_price, file=r)
            print(round(block_rate, 2), '/hr', file=r),
            print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=r)
            print('------------------------------------', file=r)
    except KeyError:
        print('scan print glitch')
        
def baserate_print(block):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    try:
        with open ("scandata/baserate", "a") as b:
            print(serviceAreaIds.stationlist[block['serviceAreaId']], file=b)
            print(date.fromtimestamp(block['startTime']).strftime('%A'), time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime'])), file=b)
            print(round(block_length, 1), 'Hours', file=b)
            print('$',block_price, file=b)
            print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=b)
            print('------------------------------------', file=b)
    except KeyError:
        print('baserate print glitch')

def caught_print(block):
        with open("scandata/scanned_blocks", "a") as f:
            print('Caught Block for', round(block['rateInfo']['priceAmount'], 1), 'Dollars', file=f)
            print('----------------------------------')

def missed_print(block):
        with open("scandata/scanned_blocks", "a") as f:
            print('Missed Block for', round(block['rateInfo']['priceAmount'], 1), 'Dollars', file=f)
            print('----------------------------------')

def request_print():
                time.sleep(1)
                with open ("scandata/token-status", "a") as d:
                    print('Token request at:', file=d)
                    print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=d)
                    print('------------------------------------', file=d)
                print('Requesting token ....', end='\r')

def blocked_print():
                with open ("scandata/token-status", "a") as d:
                    print('Token request blocked:', file=d)
                    print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=d)
                    print('------------------------------------', file=d)
                print(
                    'Authentication rejected, if your email and password is correct and you have attempted the challenge link,\n'
                    'it may not work on the device you are using.\n'
                    '\n'
                    'You can wait about 2 hours or get yor headers manually to continue.\n'
                    'There is no fix currently that I know of'
                    )