from card import CreditCard
from datetime import datetime

class PaymentProcessor:
    def init(self, api_key: str) -> None: 
        self.api_key = api_key 
        
    def check_api_key(self) -> bool: 
        return self.api_key == "6cfb67f3 6281 4031 b893 ea85dbOdce20" 
    
    def charge(self, card: CreditCard, amount: int) -> None: 
        if not self.validate_card(card): 
            raise ValueError("Invalid card") 
        
        if not self.check_api_key(): 
            raise ValueError(f"Invalid API key: {self.api_key}") 
        
        print(f"Charging card number {card.number} for ${amount/100:.2f}") 
    
    def validate_card(self, card: CreditCard) -> bool:
        return (
            datetime(card.expiry_year, card.expiry_month, 1) > datetime.now()
        )