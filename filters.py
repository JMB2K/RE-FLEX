import time

#Station Filter Values
#These are for more fine tuning of station filters, you can make this for however many stations
#upper and lower hours let you set split filters depending on the length of the block. starting at 1 and ending at 5, at incriments of .5
#rate is self explanitory, split between the two hour typs
#minimum price override allows you to accept lower rates if the total price is higher
# Be sure to add a letter at the beggining of the variables (for _lowprice, you could do T_lowprice, D_lowprice, etc. for all if you want multiple station filters)
#Sample

#time before start in hours
_headstart = 2
#rate for upper hours
_mainrate = 31
#upper hour minimum
_mainlength = 4
#rate for lower hours
_subrate = 31
#lower hour maximum
_sublength = 3.5
#minimum price override
_lowprice = 100

def simple_filter(block):
    # Filtering out blocks that you don't want.
    # Comment out individual filters that you don't want applied
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_headstart = block["startTime"] - int(time.time())
    block_rate = block_price / block_length
    return (
        block_rate > 18
        and not block["hidden"]
        #and block_price > 110
        #and block_headstart >= 1500
        #and block_length < 5
    )

def advanced_filter(block):
    #You can use a number of combinations here
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_headstart = block["startTime"] - int(time.time())
    block_rate = block_price / block_length
    block_station = block['serviceAreaId']
    # You can copy the code below and past for however many stations you want special filters for
    # Be sure to add a letter at the beggining of the variables (for _lowprice, you could do T_lowprice, D_lowprice, etc. for all)
    # identify Station
    if block['serviceAreaId'] == '8c81c54f-6a60-405c-b095-43d9b9bc99c2' and block_headstart >= _headstart*3600 and not block["hidden"]:#Sample
        if block_price < _lowprice:
            if block_length >= _mainlength:
                return (
                    block_rate >= _mainrate
                )
            if block_length <= _sublength:
                return (
                    block_rate >= _subrate
                )
        else:
            return(
                block_price >= _lowprice
            )

def print_filter(block):
    # Comment out the second line if you want to print base rate
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_headstart = block["startTime"] - int(time.time())
    block_rate = block_price / block_length
    return (
        not block["hidden"]
        and block_rate > 18
    )

def baserate_filter(block):
    # Comment out the second line if you want to print base rate
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_headstart = block["startTime"] - int(time.time())
    block_rate = block_price / block_length
    return (
        #not block["hidden"]
        block_rate == 18
    )
