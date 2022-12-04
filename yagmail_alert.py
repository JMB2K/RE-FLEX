from datetime import date
import time

try:
    import userdata.serviceAreaIds as serviceAreaIds
except:
    pass

try:
    import yagmail
except:
    pass
try:
    yag = yagmail.SMTP(user="extra-email", password="app-password")
except:
    pass

subject = "Work Available"

def email_alert(block):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_rate = block_price / block_length
    block_start = f"{date.fromtimestamp(block['startTime']).strftime('%A')} {time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime']))}"
    station_name = serviceAreaIds.stationlist[block['serviceAreaId']]
    body = f"**CAUGHT A BLOCK**\n\nLocation: {station_name}\nPay: ${block_price}\nStart Time: {block_start}\nBlock Length: {block_length} hours\nRate: {round(block_rate, 2)}"
    try:
        yag.send(to='main-email', subject=subject, contents=body)
    except:
        pass