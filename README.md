# RE-FLEX

Script for accepting work based on desired criteria, requires set up before use

As with anything PROCEED AT YOUR OWN RISK

'userdata' folder is dummy info, you'll need to get the info for header_data.py, json_data.py and registration_data.py through proxy (mitmproxy will be used in this guide but you can lso use pcap or charles proxy).

You can generate a dictionary for station names using runforstationlist.py, but only after initializing the script for the first time (since you will generate your 'user' and 'pw' file for your credentials. You may also make these files yourself and put the required info email in 'user' and password in 'pw' no extension, or just write it into the code itself in getAuth.py. Working to make stationlist generation more streamlined)

Setup for Unique Identifiers:

Download MITMProxy: https://mitmproxy.org/

Install, once installed, you will be using MITMWeb:
![image](https://user-images.githubusercontent.com/31253518/205303077-bc21e9d3-be1d-4168-a8de-1493c1c5d231.png)

List of URLs to get from proxy for setup:

Device Info (not sure for iPhone):https://switchyard-na.amazon.com/distribution/app/AmazonFlexAndroidConfig
![image](https://user-images.githubusercontent.com/31253518/205306830-2bd6ea18-d4b9-4a91-bc84-2bf74d21b8b0.png)
Be sure to change the view to JSON so you can read it

ServiceAreaId:https://flex-capacity-na.amazon.com/eligibleServiceAreas
![image](https://user-images.githubusercontent.com/31253518/205308239-b3785fa5-8b18-42ca-83df-fb76e42436d2.png)
This is available in one of the other URLs
This is for MIAMI-WEST PALM BEACH by the way

Device Serial Number:https://odcs-na-extern.amazon.com/external/GetActiveDeviceForUserExternal
![image](https://user-images.githubusercontent.com/31253518/205308763-3f65750b-7776-4cb0-a596-faa31ca910b8.png)
"deviceTypeId" tells what device you are using, this one is for Android

For header_data.py and json_data.py(if filters applied):https://flex-capacity-na.amazon.com/GetOffersForProviderPost
![image](https://user-images.githubusercontent.com/31253518/205309982-90d70031-e8b3-4abb-bf45-1d4076287964.png)
Copy the curl to here and get this:
![image](https://user-images.githubusercontent.com/31253518/205310692-610d6a31-7013-477f-bd52-0548eaca01ba.png)

After you get the required info for these:
![image](https://user-images.githubusercontent.com/31253518/205313197-583ab7f7-19ee-4875-8a63-713c4ea8146c.png)

The two Device URLs are needed for registration data,

Device info has:

"device-type"

"os-version" = "api-level"

"device_model"

and Device Serial Number has:

device_serial

Make sure app version matches, incorrect headers could lead to detection.

We were unable to find domain name but came to the conclusion it was the first item for "User-Agent" in Parenthesis, so in androids case, "Linux"
included is a script (once you have the 'user' and 'pw' files) that will generate your station list. Check for any utf-8 codes as those won't allow the script to work.

As of writing this, the script is working consistently.

Still under development
