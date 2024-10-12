# Function to save uploaded files and return file paths
import os
import uuid
from typing import List, Optional
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
from fastapi import UploadFile

from .document_forming.core import DocFormater

directory_path = "uploads/"
DOC_FORMATTER = DocFormater()

# Check if the directory exists
if not os.path.exists(directory_path):
    # Create the directory if it doesn't exist
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
else:
    print(f"Directory already exists: {directory_path}")


async def save_files(files: List[UploadFile], appeal_uuid: uuid.UUID):
    saved_paths = []
    for file in files:
        file_extension = file.filename.split(".")[-1]
        # Generate a unique file name using the appeal UUID and the file name
        file_path = os.path.join(directory_path, f"{appeal_uuid}_{file.filename}")
        saved_paths.append(file_path)
        # Save file to disk
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    return saved_paths


class TemplateData(BaseModel):
    appeal_order: Optional[str]
    executor_name: Optional[str]
    executor_phone: Optional[str]
    executor_address: Optional[str]
    customer_name: Optional[str]
    customer_address: Optional[str]
    customer_phone: Optional[str]
    laptop_firm: Optional[str]
    laptop_model: Optional[str]
    laptop_serial_number: Optional[str]
    commission_date: Optional[str]
    created_at: Optional[str]
    content: Optional[str]

class DefectClass(BaseModel):
    name: str
    coords: list

class Image(BaseModel):
    defect_photo_path: str
    defects: List[DefectClass]

class ImagesList(BaseModel):
    content: List[Image]

async def save_template(template_data: TemplateData, images_list: ImagesList):
    data = {
        'appeal_order': template_data.get("appeal_order", "12345"),
        'executor_name': template_data.get("executor_name", "Иванов Иван"),
        'executor_phone':  template_data.get("executor_phone", "8987654321"),
        'executor_address':  template_data.get("executor_address", "ул. Ленина, д. 1"),
        'customer_name':  template_data.get("customer_name", "Алексеев Алексей"),
        'customer_address':  template_data.get("customer_address", "ул. Красного знамени, д. 1"),
        'customer_phone':  template_data.get("customer_phone", "8987654321"),
        'laptop_firm': template_data.get("laptop_firm", "СИЛА"),
        'laptop_model': template_data.get("laptop_model", "НК2-3204"),
        'laptop_serial_number': template_data.get("laptop_serial_number", "F987654321"),
        'commission_date': template_data.get("commission_date", "8987654321"),
        'created_at': template_data.get("created_at", datetime.now()),
        'content': images_list,
    }
    # Returns save file path
    return DOC_FORMATTER.make_and_save_document(data)