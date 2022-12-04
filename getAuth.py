import requests
import uuid
from uuid import UUID
import getpass
import header_data
import time

def getTwoStepVerificationChallengeUrl(challengeRequest):
    verificationChallengeCode = (
        challengeRequest.get("response")
        .get("challenge")
        .get("uri")
        .split("?")[1]
        .split("=")[1]
    )
    return (
        "https://www.amazon.com/ap/challenge?openid.return_to=https://www.amazon.com/ap/maplanding&openid.oa2.code_challenge_method=S256&openid.assoc_handle=amzn_device_ios_us&pageId=amzn_device_ios_light&accountStatusPolicy=P1&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.mode=checkid_setup&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.ns.oa2=http://www.amazon.com/ap/ext/oauth/2&openid.oa2.client_id=device:30324244334531423246314134354635394236443142424234413744443936452341334e5748585451344542435a53&language=en_US&openid.ns.pape=http://specs.openid.net/extensions/pape/1.0&openid.oa2.code_challenge=n76GtDRiGSvq-Bhrez9x0CypsZFB_7eLfEDy_qZtqFk&openid.oa2.scope=device_auth_access&openid.ns=http://specs.openid.net/auth/2.0&openid.pape.max_auth_age=0&openid.oa2.response_type=code"
        + f"&arb={verificationChallengeCode}"
    )

def uuid_to_hex(uuid):
    return UUID(uuid).hex


def uuid_make():
    return(str(uuid.uuid4()))

def getAuthToken():
    user, pw = loginCode()
    """
    Get authorization token for Flex Capacity requests
    Returns:
    An access token as a string
    """
    authUrl = "https://api.amazon.com/auth/register"

    authHeaders = {
        "x-amzn-identity-auth-domain": "api.amazon.com",
        "User-Agent": "AmazonWebView/Amazon Flex/0.0/iOS/15.2/iPhone",
    }

    payload = {
        "requested_extensions": ["device_info", "customer_info"],
        "cookies": {"website_cookies": [], "domain": ".amazon.com"},
        "registration_data": {
            "domain": "Device",
            "app_version": "0.0",
            "device_type": "A3NWHXTQ4EBCZS",
            "os_version": "15.2",
            "device_serial": "0000000000000000",
            "device_model": "iPhone",
            "app_name": "Amazon Flex",
            "software_version": "1",
        },
        "auth_data": {
            "user_id_password": {
                "user_id": user,
                "password": pw,
            }
        },
        "user_context_map": {"frc": ""},
        "requested_token_type": ["bearer", "mac_dms", "website_cookies"],
    }
    #'''
    try:
        payload["registration_data"]["device_serial"] = check_device_serial()
    except:
        make_device_serial()
        payload["registration_data"]["device_serial"] = check_device_serial()
    #'''
    response = requests.post(authUrl, headers=authHeaders, json=payload).json()
    try:
        return (
            response.get("response")
            .get("success")
            .get("tokens")
            .get("bearer")
            .get("access_token")
        )
    
    except Exception as e:
        #print(response)
        #
        twoStepVerificationChallengeUrl = getTwoStepVerificationChallengeUrl(response)
        print(
            f"\n\033[1m{twoStepVerificationChallengeUrl}\033[0m "
        )
        print('\n'
        'Try the link above(preferably on the device running the code, but I am not sure),\n'
        'if it does not work, you can get your token from proxy and add it bellow\n'
        )
        #
        raise

def check_device_serial():
    with open("userdata/device_serial", "r") as d:
        dserial = d.read()
    return(dserial)

def make_device_serial():
    with open("userdata/device_serial", "w") as s:
        dserial = input('Enter deviceSerialNumber:')
        print(dserial, end='', file=s)

def requestIdSelfSingleUse():
    return (
        str(uuid.uuid4())
    )

def manualTokenRefresh():
    token = input('Enter Access Token  :')
    return(token)

def getUserLogin():
    email = input('Enter Email........ :')
    password = getpass.getpass('Enter Password :')
    return(email, password)

def printUserLogin():
    user, pw = getUserLogin()
    with open("userdata/user", "w") as u:
        print(user,  end='', file=u)
    with open("userdata/pw", "w") as p:
        print(pw,  end='', file=p)

def readUserLogin():
    with open("userdata/user", "r") as u:
        user = u.read()
    with open("userdata/pw", "r") as p:
        pw = p.read()
    return(user, pw)

def loginCode():
    try:
        user_id, password = readUserLogin()
        return(user_id, password)
    except:
        printUserLogin()
        user_id, password = readUserLogin()
        return(user_id, password)

#getAuthToken()