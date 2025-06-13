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

print(scrapped_data.info()) # why is grupakap an int?
print(scrapped_data['A_GRUPKAP'].unique()) # id from the system