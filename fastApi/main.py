import json
import os
import uuid
from contextlib import asynccontextmanager
from typing import List

import loguru
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecations
from starlette.responses import FileResponse

from fastApi.auxilary_function.document_forming.core import DocFormater
from fastApi.auxilary_function.format_appeal_response import format_appeal_response
from fastApi.auxilary_function.model_connecter import model_usage
from fastApi.auxilary_function.save_files import save_files
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from fastApi.services.appeal_operations.schemas import UpdateAppealRequest
from services.appeal_operations.models import *

deprecations.SILENCE_UBER_WARNING = True

app = FastAPI(
    title="Механик"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_db()


@app.post("/add_data/")
async def upload_data(
        firmName: str = Form(...),
        modelName: str = Form(...),
        expluatationDate: str = Form(...),
        serialNumber: str = Form(...),
        clientName: str = Form(...),
        clientPhone: str = Form(...),
        clientAddress: str = Form(...),
        clientDefects: str = Form(...),
        executorName: str = Form(...),
        executorPhone: str = Form(...),
        serviceCenterAddress: str = Form(...),
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db)
):
    # Create customer
    customer = Customer(
        name=clientName,
        phone_number=clientPhone,
        address=clientAddress
    )

    # Create executor
    executor = Executor(
        name=executorName,
        phone_number=executorPhone,
        address=serviceCenterAddress
    )

    # Save the uploaded files and get their paths
    file_paths = await save_files(files)  # Ensure this returns correct paths

    # Call the model to process the files and get defect boxes and classes (if needed)
    boxes = []  # List to hold bounding boxes
    classes = []  # List to hold defect classes

    # Process each file to get boxes and classes
    for file in file_paths:
        box, defect_class = model_usage(file)
        boxes.append(box if box else [[]])  # Ensure it returns a list
        classes.append(defect_class if defect_class else ["unknown"])

    print(f"Boxes: {boxes}")
    print(f"Classes: {classes}")
    # Create appeal
    appeal = Appeal(
        laptop_firm=firmName,
        laptop_model=modelName,
        commission_date=expluatationDate,
        laptop_serial_number=serialNumber,
        customer_text=clientDefects,
        customer=customer,
        executor=executor
    )


    print("Loading")
    # Add to session and commit
    db.add(customer)
    db.add(executor)
    db.add(appeal)
    db.commit()  # Commit to generate the UUID for appeal

    # Create result after the appeal is committed
    result = Result(
        appeal_id=appeal.uuid,
        defect_photo_path=file_paths,  # This should be a list of file paths
        defect_coords=boxes,  # Store list of boxes
        defect_class=classes  # Store list of classes
    )
    db.add(result)


    db.commit()
    return {"result_uuid": "succeed"}


@app.get("/result/{uuid}")
def get_appeal_by_uuid(uuid: str, db: Session = Depends(get_db)):
    # Fetch the appeal by UUID
    appeal = db.query(Appeal).filter(Appeal.uuid == uuid).first()
    if not appeal:
        raise HTTPException(status_code=404, detail="Appeal not found")

    # Fetch the corresponding result by appeal_id
    result = db.query(Result).filter(Result.appeal_id == appeal.uuid).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found for this appeal")

    # Format and return the response
    print (appeal, result)
    return format_appeal_response(appeal, result)


@app.get("/result/uuids/")
def get_all_uuids(db: Session = Depends(get_db)):
    # Fetch all appeals and extract their UUIDs
    appeals = db.query(Appeal).all()
    uuids = [str(appeal.uuid) for appeal in appeals]
    order = [str(appeal.order_id) for appeal in appeals]
    return {"uuids": json.dumps(uuids), "order": json.dumps(order)}


@app.get("/doc_by_uuid/{uuid}")
async def get_doc_by_uuid(uuid: str, db: Session = Depends(get_db)):
    # Fetch the appeal by UUID
    appeal = db.query(Appeal).filter(Appeal.uuid == uuid).first()

    if not appeal:
        raise HTTPException(status_code=404, detail="Appeal not found")

    # Fetch the corresponding result by appeal_id
    result = db.query(Result).filter(Result.appeal_id == appeal.uuid).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found for this appeal")

    executor = db.query(Executor).filter(Executor.uuid == appeal.executor_id).first()
    if not executor:
        raise HTTPException(status_code=404, detail="Executor not found for this appeal")

    customer = db.query(Customer).filter(Customer.uuid == appeal.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found for this appeal")

    # Prepare the data for the document
    template_data = {
        'appeal_order': str(appeal.order_id),
        'executor_name': executor.name,
        'executor_phone': executor.phone_number,
        'executor_address': executor.address,
        'customer_name': customer.name,
        'customer_address': customer.address,
        'customer_phone': customer.phone_number,
        'laptop_firm': appeal.laptop_firm,
        'laptop_model': appeal.laptop_model,
        'laptop_serial_number': appeal.laptop_serial_number,
        'commission_date': appeal.commission_date,
        'created_at': datetime.now().strftime('%Y-%m-%d'),

        # Prepare content with photos and defect details
        'content': [
            {
                "photo": file_path,  # Check if file path exists
                "defects": [
                    {
                        "coords": box,
                        "name": defect_class
                    }
                    for box, defect_class in zip(result.defect_coords, result.defect_class)
                ]
            }
            for file_path in result.defect_photo_path  # Ensure it's a valid list of paths
        ]
    }

    # Create an instance of DocFormater
    doc_formater = DocFormater()

    # Generate and save the document
    save_path = doc_formater.make_and_save_document(template_data)

    # Return the generated document as a response
    return FileResponse(save_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=os.path.basename(save_path))


@app.put("/update_appeal/{uuid}")
async def update_appeal(uuid: str, update_data: UpdateAppealRequest, db: Session = Depends(get_db)):
    # Fetch the appeal by UUID
    appeal = db.query(Appeal).filter(Appeal.uuid == uuid).first()
    if not appeal:
        raise HTTPException(status_code=404, detail="Appeal not found")

    # Update the customer details
    customer = db.query(Customer).filter(Customer.uuid == appeal.customer_id).first()
    if update_data.clientName:
        customer.name = update_data.clientName
    if update_data.clientPhone:
        customer.phone_number = update_data.clientPhone
    if update_data.clientAddress:
        customer.address = update_data.clientAddress

    # Update the executor details
    executor = db.query(Executor).filter(Executor.uuid == appeal.executor_id).first()
    if update_data.executorName:
        executor.name = update_data.executorName
    if update_data.executorPhone:
        executor.phone_number = update_data.executorPhone
    if update_data.serviceCenterAddress:
        executor.address = update_data.serviceCenterAddress

    # Update the appeal details
    if update_data.firmName:
        appeal.laptop_firm = update_data.firmName
    if update_data.modelName:
        appeal.laptop_model = update_data.modelName
    if update_data.expluatationDate:
        appeal.commission_date = update_data.expluatationDate
    if update_data.serialNumber:
        appeal.laptop_serial_number = update_data.serialNumber
    if update_data.clientDefects:
        appeal.customer_text = update_data.clientDefects

    # Commit changes to the database
    db.commit()

    return {"message": "Appeal updated successfully", "appeal": str(appeal.uuid)}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
