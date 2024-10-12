from sqlalchemy.orm import Session

from services.appeal_operations.schemas import *
from services.appeal_operations.models import *
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
#from services.appeal_operations.router import router as router_operations

app = FastAPI(
    title="Механик"
)
#app.mount("/result_imgs", StaticFiles(directory="img"), name="img")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(
#     router_operations
# )


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     get_db()


@app.post("/add_data/", response_model=DataBase)
async def add_data(data: DataBase, db: AsyncSession = Depends(get_db)):
    # db_customer = Customer(
    #     name=data.clientName,
    #     phone_number=data.clientPhone,
    #     address=data.clientAddress
    # )
    # db.add(db_customer)
    # await db.commit()
    # await db.refresh(db_customer)
    #
    # db_executor = Executor(
    #     name=data.executorName,
    #     phone_number=data.executorPhone,
    #     address=data.serviceCenterAddress
    # )
    # db.add(db_executor)
    # await db.commit()
    # await db.refresh(db_executor)
    #
    # db_appeal = Appeal(
    #     customer_id=db_customer.uuid,
    #     executor_id=db_executor.uuid,
    #     laptop_serial_number=data.serialNumber,
    #     laptop_firm=data.firmName,
    #     laptop_model=data.modelName,
    #     commission_date=data.expluatationDate,
    #     customer_text=data.clientDefects
    # )
    # db.add(db_appeal)
    # await db.commit()
    # await db.refresh(db_appeal)
    #
    # # You'll need to add code here to create a Result object
    print(data)
    return data

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
