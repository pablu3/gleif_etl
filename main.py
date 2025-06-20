import pandas as pd
import requests as rq
import warnings
warnings.filterwarnings('ignore')

raw_data = pd.read_csv("mail.csv", sep=";")

# data required in the final database
data = raw_data[["A_LEICODE", "OSNAZWA", "CENTKRAJKOD", "CENTKRAJNAZWA", "OSADRMIEJSC", "A_GRUPKAP"]]

# inserting empty columns for data that will be extracted from the API
scrapped_data = data.copy()
scrapped_data['lei_s'] = ''
scrapped_data['nazwa_s'] = ''
scrapped_data['krajkod_s'] = ''
scrapped_data['kodp_s'] = ''
scrapped_data['direct_parent'] = ''
scrapped_data['ultimate_parent'] = ''

# main loop
for i, record in scrapped_data[['A_LEICODE']].iterrows(): # extract data based on LEI
    entity = rq.get(f'https://api.gleif.org/api/v1/lei-records/{record[0]}')
    try:
        scrapped_data['lei_s'].iloc[i] = entity.json()['data']['attributes']['lei']
        scrapped_data['nazwa_s'].iloc[i] = entity.json()['data']['attributes']['entity']['legalName']['name']
        scrapped_data['krajkod_s'].iloc[i] = entity.json()['data']['attributes']['entity']['legalAddress']['country']
        scrapped_data['miasto_s'].iloc[i] = entity.json()['data']['attributes']['entity']['legalAddress']['city']
        scrapped_data['kodp_s'].iloc[i] = entity.json()['data']['attributes']['entity']['legalAddress']['postalCode']

        # if there is a direct parent, retrieve LEI
        try:
            direct_parent = entity.json()['data']['relationships']['direct-parent']['links']['lei-record']
            dp_request = rq.get(direct_parent)
            scrapped_data['direct_parent_s'].iloc[i] = dp_request.json()['data']['attributes']['lei']
        # otherwise do nothing
        except:
            continue

        # if there is an ultimate parent, retrieve LEI
        try:
            ultimate_parent = entity.json()['data']['relationships']['ultimate-parent']['links']['lei-record']
            up_request = rq.get(ultimate_parent)
            scrapped_data['ultimate_parent_s'].iloc[i] = up_request.json()['data']['attributes']['lei']
        # otherwise do nothing
        except:
            continue
    # error handling here is still basic, TBU (handling based on response status codes)
    except:
        continue

print('scrapping complete')

# extract as .csv
scrapped_data.to_csv('scrapped_data.csv', index=False)
print('File saved successfully')