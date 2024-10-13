from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

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
    defect_photo_path: List[str]  # Change to List[str] for multiple photo paths
    defect_coords: List[List[List[int]]]  # Change to List[List[int]] for nested coordinates
    defect_class: List[List[str]]  # Change to List[str] for multiple defect classes


class UpdateAppealRequest(BaseModel):
    firmName: Optional[str] = None
    modelName: Optional[str] = None
    exploitationDate: Optional[datetime] = None  # Use datetime for dates
    serialNumber: Optional[str] = None
    clientName: Optional[str] = None
    clientPhone: Optional[str] = None
    clientAddress: Optional[str] = None
    clientDefects: Optional[List[str]] = None  # List for multiple defects
    executorName: Optional[str] = None
    executorPhone: Optional[str] = None
    serviceCenterAddress: Optional[str] = None
