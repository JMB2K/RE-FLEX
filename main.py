import requests, json, time, logging ,random ,yagmail
from datetime import datetime, date
import userdata.serviceAreaIds as serviceAreaIds
import userdata.header_data as header_data
import userdata.json_data as json_data
import filters, debug, live_updates, authCycle

timehigh = 4.8
timelow = 3.8

rapidvalue = 3

rapidtimehigh = 0.4
rapidtimelow = 0.2

rapidrefresh = rapidvalue

logging.basicConfig(format="%(asctime)s \n\t%(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

yag = yagmail.SMTP(user="extra-email", password="app-password")
subject = "Work Available"

session = requests.Session()


def email_alert(block):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_rate = block_price / block_length
    block_start = f"{date.fromtimestamp(block['startTime']).strftime('%A')} {time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime']))}"
    station_name = serviceAreaIds.stationlist[block['serviceAreaId']]
    body = f"**CAUGHT A BLOCK**\n\nLocation: {station_name}\nPay: ${block_price}\nStart Time: {block_start}\nBlock Length: {block_length} hours\nRate: {round(block_rate, 2)}"
    yag.send(to='main-email', subject=subject, contents=body)

print('Scanning started at', time.strftime('%I:%M:%S %p'))

def get_offer_list():
    # Requesting list of available blocks and returning either a filtered list of blocks or an error message
    authCycle.requestId_refresh()
    global session
    response = session.post(
        "https://flex-capacity-na.amazon.com/GetOffersForProviderPost",
        headers=header_data.headers,
        json=json_data.search_json_data,
    )

    j = json.loads(response.text)
    try:
        for block in j['offerList']:
            if(rapidrefresh>=rapidvalue):
                live_mode(block)
            if(rapidrefresh<rapidvalue):
                live_rapid(block)
        return [accept_block(block) for block in j["offerList"] if filters.advanced_filter(block)]
    except KeyError:
        try:
            return j["message"]
        except KeyError:
            print('Disconnected.........', end='\r')
            pass

def live_mode(block):
    if filters.advanced_filter(block):
        # Comment or uncomment bellow if you want to disable certain features
        live_updates.live_mode(block)
        live_updates.print_history(block)
    if filters.print_filter(block):
        debug.scan_print(block)
    #if filters.baserate_filter(block):
        #debug.baserate_print(block)

def live_rapid(block):
    if filters.advanced_filter(block):
        # Comment or uncomment bellow if you want to disable certain features
        live_updates.live_rapid(block)
        #live_updates.rapid_history(block)


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
            if(rapidrefresh<rapidvalue):
                rapidrefresh+=1
                time.sleep(random.uniform(rapidtimelow, rapidtimehigh))
            else:
                time.sleep(random.uniform(timelow, timehigh))
