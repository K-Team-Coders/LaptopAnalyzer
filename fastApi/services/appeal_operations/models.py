from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, BigInteger, Text, JSON, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime
metadata = MetaData()

customers = Table(
    "customers",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False, unique = True),
    Column("phone_number", String, nullable=False),
    Column("address", String, nullable=False),
)

executors = Table(
    "executors",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False, unique = True),
    Column("phone_number", String, nullable=False),
    Column("address", String, nullable=False),
)

appeals = Table(
    "appeals",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key = True, default = uuid.uuid4),
    Column("ordel_id", BigInteger, unique = True, autoincrement = True),
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.uuid")),
    Column("executor_id", UUID(as_uuid=True), ForeignKey("executors.uuid")),
    Column("laptop_serial_number", String, nullable = False),
    Column("laptop_firm", String, nullable = False),
    Column("laptop_model", String,nullable = False),
    Column("commission_date", TIMESTAMP, nullable = False),
    Column("customer_text", Text, default = ""),
    Column("created_at", DateTime, default = datetime.now()))
)

results = Table(
    "results",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key = True, default = uuid.uuid4),
    Column("appeal_id", UUID(as_uuid=True), ForeignKey("appeals.uuid")),
    Column("defect_photo_path", String, nullable = False),
    Column("defect_coords", ARRAY(Integer), nullable = False),
    Column("class", String)
)


