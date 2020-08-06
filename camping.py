import json
import requests

# Park ID
# Porpoise Bay Provincial Park = 167
park_id = 167

# Date
date = '2020-08-15T00:00:00'


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

    result = r.json()
    units = result['Facility']['Units']

    all_sites = map(lambda x: { 'Name': units[x]['Name'], 'Slices': units[x]['Slices'][date] }, units)

    # filter out walk-in sites since they are always marked as empty
    non_walkin = filter(lambda x: not x['Slices']['IsWalkin'], all_sites)

    # filter out reserved sites
    empty_sites = list(filter(lambda x: x['Slices']['IsFree'], non_walkin))

    if len(empty_sites) == 0:
        print('All the sites are reserved :\'-(')
    else:
        for site in empty_sites:
            print(site['Name'] + ' is empty!!!!')
