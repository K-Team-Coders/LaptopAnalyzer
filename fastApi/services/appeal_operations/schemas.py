from datetime import date
import re
from pydantic import BaseModel,  Field, ValidationError, validator

class CreateAppeal(BaseModel):
    laptop_serial_number: str = Field(default=..., min_length=3, max_length=10)
    laptop_firm: str = Field(default=..., min_length=1, max_length=15)
    laptop_model: str = Field(default=..., min_length=1, max_length=15)
    customer_name: str = Field(default=..., min_length=1, max_length=60)
    customer_phone: str = Field(default=...)
    customer_address: str = Field(min_length=10, max_length=200)
    executor_name: str = Field(default=..., min_length=1, max_length=60)
    executor_phone: str = Field(default=...)
    executor_address: str = Field(default=..., min_length=10, max_length=100)
    executor_address: str = Field(default=..., min_length=10, max_length=100)
    comission_date: date = Field(default=... , )
    
    
    @validator('customer_phone', "executor_phone")
    def format_phone(cls, value):
        digits = re.sub(r'\D', '', value)

        if len(digits) == 10:
            return f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"
        elif len(digits) == 11 and digits.startswith('7') or digits.startswith('8'):
            return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
        elif len(digits) == 12 and digits.startswith('8'):
            digits = '7' + digits[1:]  # Заменяем 8 на 7
            return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
        else:
            raise ValueError('Invalid phone number format')
    

