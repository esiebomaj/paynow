import requests
from paynow import settings

secret_key = settings.PAYSTACK_SECRET_KEY
public_key = settings.PAYSTACK_PUBLIC_KEY

class Paystack(object):
    SUCESS_STATUS = "success"
    def __init__(self, **kwargs):
        self.client = requests.Session()
        self.client.headers["Authorization"] = "Bearer " + secret_key

    def init_transaction(self, data):
        url = "https://api.paystack.co/transaction/initialize"
        res = self.client.post(url, data)
        print(res, res.json())
        res.raise_for_status()
        return res.json()["data"]

    def verify_transaction(self, data):
        url = "https://api.paystack.co/transaction/verify/{}".format(data["reference"])
        res = self.client.get(url)
        print(res, res.json())
        res.raise_for_status()
        return res.json()

    def create_recipient(self, data):
        url = "https://api.paystack.co/transferrecipient"
        res = self.client.post(url, data)
        print(res, res.json())
        res.raise_for_status()
        return res.json()

    def deposit_to_bank(self, data):
        url = "https://api.paystack.co/transfer"
        res = self.client.post(url, data)
        print(res, res.json())
        res.raise_for_status()
        return res.json()

    def get_list_of_banks(self):
        url = "https://api.paystack.co/bank?currency=NGN"
        res = self.client.get(url)
        print(res, res.json())
        res.raise_for_status()
        return res.json()
