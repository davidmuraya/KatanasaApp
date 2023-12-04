from pydantic import BaseModel


class SafaricomIPAddresses(BaseModel):
    c2b_callback_ip_addresses: list = ["196.201.214.200", "196.201.214.206", "196.201.213.114",
                                       "196.201.214.207", "196.201.214.208", "196.201.213.44",
                                       "196.201.212.127", "196.201.212.138", "196.201.212.129",
                                       "196.201.212.136", "196.201.212.74", "196.201.212.69"]


ip_addresses = SafaricomIPAddresses()
