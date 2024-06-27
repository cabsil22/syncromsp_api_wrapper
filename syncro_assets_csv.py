""" You will need permissions in Syncro for your api key:


 Usage:

 syncro_assets_csv.py <customer_id> assets.csv

 """

from syncromsp_api_wrapper import SyncroAPI
import csv
import sys

#you can use an Environment variable to store you api key if you want
api = SyncroAPI("subdomain", "YOUR API KEY")

def import_assets_csv(customer_id: int, file:str):
    with open(file, 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            asset = {'asset_type_id': row['type'],
                     'name': row['asset_name'], 'customer_id': row['customer'], 'asset_serial': row['asset_serial']}
            if 'contact_id' in row:
                if row['contact_id']:
                    asset['contact_id'] = row['contact_id']
            print(api.post_asset(asset))

def run(customer_id: int, file: str):
        input(f'I am going to import assets to customerID: {str(customer_id)} from file: {str(file)}')
        try:
            import_assets_csv(customer_id, file)
        except Exception as e:
            print(e)

# if script is called from command line
if __name__ == "__main__":
    run(str(sys.argv[1]), int(sys.argv[2]))



