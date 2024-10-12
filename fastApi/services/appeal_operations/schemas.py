from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date


class CustomerBase(BaseModel):
    name: str
    phone_number: str
    address: str


class ExecutorBase(BaseModel):
    name: str
    phone_number: str
    address: str


class AppealBase(BaseModel):
    customer_id: UUID
    executor_id: UUID
    laptop_serial_number: str
    laptop_firm: str
    laptop_model: str
    commission_date: datetime
    customer_text: str = ""


class ResultBase(BaseModel):
    appeal_id: UUID
    defect_photo_path: str
    defect_coords: list[int]
    defect_class: str



