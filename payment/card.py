from dataclasses import dataclass 

class CreditCard:
    number: str 
    expiry_month: int 
    expiry_year: int
    
    def __init__(self, number, expiry_month, expiry_year):
        self.number = number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year