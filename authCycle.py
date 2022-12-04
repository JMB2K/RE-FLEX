import getAuth
import header_data
import json_data
import getServiceAreas
import time
import debug
import uuid




def header_refresh():
    with open("userdata/token", "w") as t:
        print(getAuth.getAuthToken(),  end='', file=t)
    current_header()

def current_header():
    with open("userdata/token", "r") as t:
        token = t.read()
        header_data.headers['x-amz-access-token'] = token

def requestId_refresh():
    header_data.headers['X-Amzn-RequestId'] = getAuth.requestIdSelfSingleUse()

def manual_token():
        token = getAuth.manualTokenRefresh()
        header_data.headers['x-amz-access-token'] = token
        with open('userdata/token', 'w') as t:
            print(token, end='', file=t)

def test():
    lst = getServiceAreas.getEligibleServiceAreas()
    if None in lst:
        print('Token expired........', end='\r')
        time.sleep(1)
        raise Exception
    else:
        pass


def authCycle():
    try:
        print('Reading from file ...', end='\r')
        time.sleep(1)
        current_header()
        test()
    except:
        try:
            debug.request_print()
            header_refresh()
        except:
            debug.blocked_print()
            manual_token()


def instance_check():
    with open("userdata/instance_id", "r") as i:
        instanceId = i.read()
        return(instanceId)

def instance_make():
    with open("userdata/instance_id", "w") as i:
        instanceId = str(uuid.uuid4())
        print(instanceId, end='', file=i)

def instanceCycle():
    try:
        instance_check()
    except:
        instance_make()
        instance_check()

def areaId_check():
    with open("userdata/areaId.py", "r") as i:
        areaId = i.read()
        return(areaId)

def areaId_grab():
    with open("userdata/areaId.py", "w") as i:
        areaId = getServiceAreas.getEligibleServiceAreas()
        print('areaId =', areaId, end='', file=i)

def areaIdCycle():
    try:
        import userdata.areaId as areaId
    except:
        areaId_grab()
        import userdata.areaId as areaId
        json_data.search_json_data["serviceAreaIds"] = areaId.areaId
    json_data.search_json_data["serviceAreaIds"] = areaId.areaId