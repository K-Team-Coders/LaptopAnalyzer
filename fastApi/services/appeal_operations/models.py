import uuid
from sqlalchemy import Table, Column, String, ForeignKey, DateTime, BigInteger, TIMESTAMP, Text, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)

    appeals = relationship("Appeal", back_populates="customer")


class Executor(Base):
    __tablename__ = "executors"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)

    appeals = relationship("Appeal", back_populates="executor")


class Appeal(Base):
    __tablename__ = "appeals"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    order_id = Column(BigInteger, unique=True, autoincrement=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.uuid"))
    executor_id = Column(UUID(as_uuid=True), ForeignKey("executors.uuid"))
    laptop_serial_number = Column(String, nullable=False)
    laptop_firm = Column(String, nullable=False)
    laptop_model = Column(String, nullable=False)
    commission_date = Column(String, nullable=False)
    customer_text = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)

    customer = relationship("Customer", back_populates="appeals")
    executor = relationship("Executor", back_populates="appeals")
    results = relationship("Result", back_populates="appeal")


class Result(Base):
    __tablename__ = "results"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appeal_id = Column(UUID(as_uuid=True), ForeignKey("appeals.uuid"))
    defect_photo_path = Column(String, nullable=False)
    defect_coords = Column(ARRAY(Integer), nullable=False)
    defect_class = Column(String)

    appeal = relationship("Appeal", back_populates="results")
