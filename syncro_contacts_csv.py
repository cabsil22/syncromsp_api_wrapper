""" You will need the following permissions in Syncro for your api key:
 Customers - View Detail Single
 Customers - Edit Single

 Usage:

 syncro_contacts_csv.py import <customer_id> contacts.csv
 syncro_contacts_csv.py export <customer_id> contacts.csv
 """

from syncromsp_api_wrapper import SyncroAPI
import csv
import sys
api = SyncroAPI("subdomain", "YOUR API KEY")


def export_contacts_csv(customer_id: int, file:str):

    contacts = api.get_contacts_from_customer(customer_id)
    with open(file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        header_count = 0
        for contact in contacts:
            if header_count < 1:
                w.writerow(contact.keys())
                header_count += 1
            w.writerow(contact.values())


def import_contacts_csv(customer_id: int, file:str):
    with open(file, 'r') as f:
        r = csv.DictReader(f)

        for row in r:
            contact = {'customer_id': customer_id, 'name': row['name'], 'address1': row['address1'],
                       'address2': row['address2'], 'city': row['city'], 'state': row['state'], 'zip': row['zip'],
                       'email': row['email'], 'phone': row['phone'], 'mobile': row['mobile'], 'notes': row['notes']}
            print(api.post_contact(contact))


def run(mode: str, customer_id: int, file: str):

    if mode == "import":
        print(f'I am going to {str(mode)} contacts to {str(customer_id)} from {str(file)}')
        import_contacts_csv(customer_id, file)
    elif mode == "export":
        print(f'I am going to {str(mode)} contacts from {str(customer_id)} to {str(file)}')
        export_contacts_csv(customer_id, file)
    else:
        print("Unknown mode type")


if __name__ == "__main__":
    run(str(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]))
