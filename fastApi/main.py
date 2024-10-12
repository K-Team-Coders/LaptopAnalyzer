from contextlib import asynccontextmanager
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.util import deprecations

from fastApi.auxilary_function.format_appeal_response import format_appeal_response
from fastApi.auxilary_function.model_connecter import model_usage
from fastApi.auxilary_function.save_files import save_files
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
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
    shared_uuid = uuid.uuid4()

    # Create customer
    customer = Customer(
        uuid=shared_uuid,
        name=clientName,
        phone_number=clientPhone,
        address=clientAddress
    )

    # Create executor
    executor = Executor(
        uuid=shared_uuid,
        name=executorName,
        phone_number=executorPhone,
        address=serviceCenterAddress
    )

    # Save the uploaded files and get their paths
    file_paths = await save_files(files, shared_uuid)
    boxes = list()
    classes = list()

    for file in file_paths:
        boxes.append, classes.append(model_usage(file))  # Вызов функции для использования модели машинки
    uuid_for_appeal = uuid.uuid4()
    # Create appeal

    appeal = Appeal(
        uuid=uuid_for_appeal,
        laptop_firm=firmName,
        laptop_model=modelName,
        commission_date=expluatationDate,
        laptop_serial_number=serialNumber,
        customer_text=clientDefects,
        customer=customer,
        executor=executor,
        file_paths=file_paths
    )
    boxes, classes = model_usage()  # Вызов функции для использования модели машинки
    # Добавление обработки машинкой и отправка результата

    # Add to session and commit
    db.add(customer)
    db.add(executor)
    db.add(appeal)
    result = Result(
        uuid=uuid.uuid4(),
        appeal_id=uuid_for_appeal,
        defect_photo_path=file_paths,
        defect_coords=boxes,
        defect_class=classes
    )

    db.add(result)

    await db.commit()

    return {"result_uuid": str(result.uuid)}


@app.get("/appeal/{uuid}")
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
    return format_appeal_response(appeal, result)


# 2. Route to get all UUIDs from the database
@app.get("/appeals/uuids/")
def get_all_uuids(db: Session = Depends(get_db)):
    # Fetch all appeals and extract their UUIDs
    appeals = db.query(Appeal).all()
    uuids = [str(appeal.uuid) for appeal in appeals]

    return {"uuids": uuids}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
