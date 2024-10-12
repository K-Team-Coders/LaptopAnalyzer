from contextlib import asynccontextmanager
from typing import List
from fastApi.auxilary_function.save_files import save_files
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from services.appeal_operations.models import *

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
        files: List[UploadFile] = File(...)
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

    # Create appeal
    appeal = Appeal(
        uuid=shared_uuid,
        laptop_firm=firmName,
        laptop_model=modelName,
        commission_date=expluatationDate,
        laptop_serial_number=serialNumber,
        customer_text=clientDefects,
        customer=customer,
        executor=executor,
        file_paths=file_paths
    )
    db_session = get_db()
    # Add to session and commit
    db_session.add(customer)
    db_session.add(executor)
    db_session.add(appeal)
    await db_session.commit()
    # Добавление обработки машинкой и отправка результата
    return appeal


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
