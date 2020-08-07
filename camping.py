import json
import requests
import smtplib
import ssl


### Configurations ###

# Park ID
# Porpoise Bay Provincial Park = 167
park_id = 167

# Date
date = '2020-08-15T00:00:00'

# email related configurations
sender = 'email_address'
receiver = 'email_address'
pwd = 'password'

### End of Configurations ###

payload = {
    "FacilityId":park_id,
    "UnitTypeId":0,
    "StartDate":"08-06-2020",
    "InSeasonOnly": True,
    "WebOnly":True,
    "IsADA":False,
    "SleepingUnitId":0,
    "MinVehicleLength":0,
    "UnitCategoryId":0,
    "UnitTypesGroupIds":[],
    "MinDate":"8/5/2020",
    "MaxDate":"8/5/2021"
}

headers = {
    'Content-Type': 'application/json'
}

if __name__ == "__main__":
    r = requests.post('https://bccrdr.usedirect.com/rdr/rdr/search/grid', json.dumps(payload), headers=headers)

    if r.status_code != 200:
        print(f'Request failed with status code {r.status_code}')
        exit(1)

    units = r.json()['Facility']['Units']

    # construct a new dict to hold the needed data
    # {
    #   Name: name,
    #   Slices: Slices
    # }
    all_sites = map(lambda x: { 'Name': units[x]['Name'], 'Slices': units[x]['Slices'][date] }, units)

    # filter out walk-in sites since they are always marked as empty
    non_walkin = filter(lambda x: not x['Slices']['IsWalkin'], all_sites)

    # filter out reserved sites
    empty_sites = list(filter(lambda x: x['Slices']['IsFree'], non_walkin))

    if len(empty_sites) == 0:
        print(f'All the sites are reserved :\'-(\n')
    else:
        msg = ''
        for site in empty_sites:
            msg += site['Name'] + ' is empty!!!!\n'

        print(msg)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
            server.login(sender, pwd)
            server.sendmail(sender, receiver, msg)
