import json
import requests
import smtplib
import ssl
from pathlib import Path


### Configurations ###
placeId = "41"

day = '29'
people = 6
pad = 3

# email related configurations
sender = ''
receiver = ''
pwd = ''

### End of Configurations ###

payload = {
    "gwFacilityId":f"277_2020-08-{day}",
    "arrivalDate":f"08-{day}-2020",
    "noOfParties":people,
    "noOfPads":pad,
    "placeId":placeId
}



headers = {
    'Content-Type': 'application/json'
}

if __name__ == "__main__":
    if Path(receiver).exists():
        exit(0)

    r = requests.post('https://www.discovercamping.ca/BCCWeb/Facilities/TrailRiverCampingSearchView.aspx/LockUnitPersonOccupancy', json.dumps(payload), headers=headers)

    if r.status_code != 200:
        print(f'Request failed with status code {r.status_code}')
        exit(1)

    success = r.json()['d']['IsSuccess']

    if success:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
            server.login(sender, pwd)
            server.sendmail(sender, receiver, f'Garibaldi campsite is available on Aug. {day}!!!')

        Path(receiver).touch()
    else:
        print(r.json()['d']['ExceptionMessage'])
        print(r.json()['d']['InformationMessage'])
