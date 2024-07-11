Syncro MSP API Wrapper and a few example functions. 

# Requirements:

python requests module

python munch module (fork of Bunch that works with modern python)


# Usage:


The simplest usage:
```python
from syncromsp_api_wrapper import SyncroAPI
api = SyncroAPI("yoursubdomain", api_key="YOUR API KEY")
tickets = api.get_tickets()
for ticket in tickets:
    print(ticket.number)
```

Your api key can be specified or read from an env variable - SYNCRO_API_KEY

```python
from syncromsp_api_wrapper import SyncroAPI
api = SyncroAPI("yoursubdomain")

# some more ticklers to get you started
ticket_types = api.get_ticket_types()

for ticket_type in ticket_types:
    print(ticket_type)

ticket_status_list = api.get_ticket_status_list()

for ticket_status in ticket_status_list:
    print(ticket_status)

billing_tickets = api.get_tickets(status="Billing")

for billing_ticket in billing_tickets:
    print(f"The ticket number {billing_ticket.number} with the subject of {billing_ticket['subject']} needs to be billed.")
```


If you want to filter by parameters that have not been implemented in the api wrapper yet, you can add them to the request parameters dictionary before the request goes out.

You can see available parameters in the syncro docs: https://api-docs.syncromsp.com/#/
```python
from syncromsp_api_wrapper import SyncroAPI
api = SyncroAPI("yoursubdomain")

#all tickets created after the date
api.request_parameters['created_after'] = "2024-05-25"
tickets = api.get_tickets(status=None)
for ticket in tickets:
    print(ticket['number'])
```
The custom request parameters that you set will stay in the requests until you clear them out with the .clean() method. This means you can chain multiple requests with similar parameters easily.
```python
from syncromsp_api_wrapper import SyncroAPI
api = SyncroAPI("yoursubdomain")

#show tickets created after the date
api.request_parameters['created_after'] = "2024-05-25"
#Billing tickets created after 2024-05-25
tickets = api.get_tickets(status="Billing")
for ticket in tickets:
    print(ticket['number'])

#scheduled tickets created after 2024-05-25    
tickets = api.get_tickets(status="Scheduled")
for ticket in tickets:
    print(ticket['number'])

#all open tickets after the date
tickets = api.get_tickets()

#removes the custom parameters
api.clean()

#all open tickets
tickets = api.get_tickets()


```

# Samples

## syncro_contacts_csv.py script:

You will need the following permissions in Syncro for your api key:

Customers - View Detail Single

Customers - Edit Single
 
### Script Usage:


syncro_contacts_csv.py import <customer_id> contacts.csv

syncro_contacts_csv.py export <customer_id> contacts.csv
