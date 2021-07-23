import requests
from collections import OrderedDict


class SyncroAPI:

    def __init__(self, subdomain, api_key, server_domain=None, api_version_string=None, protocol=None, debug=False):
        self.subdomain = subdomain
        self.api_key = api_key
        self.debug = False
        self.pages = 1
        self.body = ""
        if server_domain:
            self.server_domain = server_domain
        else:
            self.server_domain = "syncromsp.com"
        if api_version_string:
            self.api_version_string = api_version_string
        else:
            self.api_version_string = "/api/v1/"
        if protocol:
            self.protocol = protocol
        else:
            self.protocol = "https"
        if debug:
            self.debug = True

        self.request_type = ""
        self.request_parameters = OrderedDict()

    def build_url(self):
        url = self.protocol + "://" + self.subdomain + "." + self.server_domain + self.api_version_string
        url += self.request_type
        url += "?"
        if len(self.request_parameters) > 0:
            if "id" in self.request_parameters:
                self.request_parameters.move_to_end('id', last=False)
            for param, value in self.request_parameters.items():
                if param == "id":
                    url = url.rstrip("?")
                    url += "/" + value
                    url += "?"
                else:
                    url += param + "=" + value + "&"

        url += "api_key=" + self.api_key
        if self.debug:
            print(url)
        return url

    def request(self):
        url = self.build_url()
        r = requests.get(url)
        return r.json()

    def post_request(self):
        url = self.build_url()
        r = requests.post(url, data=self.body)
        return r.json()


    def get_tickets(self):
        self.request_type = "tickets"
        tickets = []
        i = 1
        pages = 1
        while i <= pages:
            self.request_parameters["page"] = str(i)
            response = self.request()
            tickets.extend(response['tickets'])
            pages = response['meta']['total_pages']
            i = i + 1
        return tickets

    def get_ticket_by_id(self, ticket_id: int) -> object:
        """
        Clears request_parameters then queries by ticket_id

        :param ticket_id: int or string of the syncro ticket_id
        :return: ticket object with ticket['properties']
        """
        self.request_type = "tickets"
        self.request_parameters['id'] = str(ticket_id)
        response = self.request()
        if "ticket" not in response:
            return False
        return response['ticket']

    def get_invoices(self):
        self.request_type = "invoices"
        response = self.request()
        invoices = response['invoices']
        return invoices

    def get_invoice_by_id(self, invoice_id):
        self.request_type = "invoices"
        self.request_parameters['id'] = str(invoice_id)
        response = self.request()
        if "invoice" not in response:
            return False
        return response['invoice']

    def get_products(self):
        self.request_type = "products"
        response = self.request()
        return response['products']

    def clean(self):
        """
        Cleans the instance so it is fresh. Removes all request parameters, etc.

        :return: none
        """
        self.request_parameters = OrderedDict()
        self.request_type = ""

    def get_ticket_by_number(self, ticket_number: int) -> object:
        self.request_type = "tickets"
        self.request_parameters['number'] = str(ticket_number)
        response = self.request()
        if "tickets" not in response or len(response["tickets"]) < 1:
            return False
        return response["tickets"][0]

    def get_contacts_from_customer(self, customer_id: int):
        self.request_type = "contacts"
        self.request_parameters['customer_id'] = str(customer_id)
        contacts = []
        i = 1
        pages = 1
        while i <= pages:
            self.request_parameters["page"] = str(i)
            response = self.request()
            if self.debug:
                print(response)
            contacts.extend(response['contacts'])
            pages = response['meta']['total_pages']
            i = i + 1
        return contacts

    def post_contact(self, contact: dict):
        self.request_type = "contacts"
        self.body = contact
        response = self.post_request()
        return response

