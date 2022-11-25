import requests
import json
import time
import logging
import random
from datetime import datetime, date
import yagmail
import userdata.serviceAreaIds as serviceAreaIds
import userdata.header_data as header_data
import userdata.json_data as json_data
import filters
import debug
import live_updates
import getServiceAreas
import authCycle

rapidrefresh = 3

logging.basicConfig(format="%(asctime)s \n\t%(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

yag = yagmail.SMTP(user="extra-gmail", password="app-password")
subject = "Work Available"
session = requests.Session()


def email_alert(block):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_rate = block_price / block_length
    block_start = f"{date.fromtimestamp(block['startTime']).strftime('%A')} {time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime']))}"
    station_name = serviceAreaIds.stationlist[block['serviceAreaId']]
    body = f"**CAUGHT A BLOCK**\n\nLocation: {station_name}\nPay: ${block_price}\nStart Time: {block_start}\nBlock Length: {block_length} hours\nRate: {block_rate}"
    yag.send(to='main-email', subject=subject, contents=body)


def __getAmzDate() -> str:
    """
        Returns Amazon formatted timestamp as string
        """
    return datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

def up_DATE():
    header_data.headers["X-Amz-Date"] = __getAmzDate()

print('Scanning started at', time.strftime('%I:%M:%S %p'))


def get_offer_list():
    # Requesting list of available blocks and returning either a filtered list of blocks or an error message
    authCycle.requestId_refresh()
    #client_time()
    global session
    response = session.post(
        "https://flex-capacity-na.amazon.com/GetOffersForProviderPost",
        headers=header_data.headers,
        json=json_data.search_json_data,
    )

    j = json.loads(response.text)
    try:
        for block in j['offerList']:
            # Comment or uncomment bellow if you want to disable certain features
            live_updates.live_mode(block)
            live_updates.print_history(block)
            debug.scan_print(block)
            #debug.baserate_print(block)
        return [accept_block(block) for block in j["offerList"] if filters.advanced_filter(block)]
    except KeyError:
        try:
            return j["message"]
        except KeyError:
            print('Disconnected.........', end='\r')
            pass

def accept_block(block):
    # Accepting a block, returns status code. 200 is a successful attempt and 400 (I think, could be 404 or something else) is a failed attempt
    global session
    global rapidrefresh
    accept = session.post(
        "https://flex-capacity-na.amazon.com/AcceptOffer",
        headers=header_data.headers,
        json=json_data.accept_json_data(block["offerId"]),
    )

    if accept.status_code == 200:
        logging.info(f"Caught The Block For {block['rateInfo']['priceAmount']}")
        debug.caught_print(block)
        email_alert(block)
    else:
        logging.info(f"Missed The Block For {block['rateInfo']['priceAmount']}")
        debug.missed_print(block)
        rapidrefresh = 0

    return accept.status_code

if __name__ == "__main__":

    authCycle.authCycle()

    keepItUp = True
    while keepItUp:
            print('Scanning...', datetime.now().strftime('%S:%f'), end='\r')
            lst = get_offer_list()
            if lst == "Rate exceeded":
                logging.info("Rate Exceeded, Waiting")
                time.sleep(30)
                logging.info("Resuming operations")
            try:
                if 200 in lst:
                    keepItUp = False
                    break
            except TypeError:
                 authCycle.authCycle()
            '''
            Refresh Speed:
            Use any range for whatever speeds you are looking for
            One method recomended no lower than one second for less risk of detection,
            but would allow as low as 0.2
            With the new refresh changes, it might be best to just use a low speed to scan,
            and then when you see there are offers, use a faster speed to try and catch.
            you will end up being throttled when you reach rate limit until you
            wait, about an hour or more
            '''
            if(rapidrefresh<3):
                rapidrefresh+=1
                time.sleep(random.uniform(0.2, 0.6))
            else:
                time.sleep(random.uniform(3.8, 4.8))
                #time.sleep(random.uniform(2.8, 3.6))
                #time.sleep(random.uniform(0.8, 2.4))
                #time.sleep(random.uniform(0.2, 0.6))
