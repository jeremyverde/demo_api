from fastapi import FastAPI, status, Response
import time
from contextlib import asynccontextmanager

from src.settings import Settings
from src.logger import logger
from src.orders.router import router as orders_router
from src.users.router import router as users_router
from .schemas import TableEnum, table_map
from .data.demo_db import join_tables
from uuid import UUID

app = FastAPI()

SETTINGS = Settings()

app.include_router(orders_router)
app.include_router(users_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Startup")
    yield
    logger.info("Shutting Down, Closing DB conn")


@app.get("/health")
async def health_check():
    return {"time": time.time(), "environment": SETTINGS.env}


# requested endpoints
@app.post("/v1/add_record/{table}", status_code=status.HTTP_201_CREATED)
async def add_record(table: TableEnum, records: list[dict]):
    schema = table_map[table.value]["create_schema"]
    ta_records = [schema(**record) for record in records]
    logger.info(f"Adding record to {table.value} table")
    result = await table_map[table.value]["create_function"](ta_records)
    return result


@app.put("/v1/update_record/{table}/{record_id}", status_code=status.HTTP_200_OK)
async def update_record(
    table: TableEnum, record_id: UUID, record: dict, response: Response
):
    schema = table_map[table.value]["create_schema"]
    ta_record = schema(**record)
    logger.info(f"Updating record {record_id} in {table.value} table")
    result = await table_map[table.value]["update_function"](record_id, ta_record)
    if result is None:
        logger.info(f"Record {record_id} not found in {table.value} table")
        response.status_code = status.HTTP_404_NOT_FOUND
    return result


@app.delete(
    "/v1/delete_record/{table}/{record_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_record(table: TableEnum, record_id: UUID):
    logger.info(f"Deleting record {record_id} from {table.value} table")
    result = await table_map[table.value]["delete_function"](record_id)
    if result is None:
        logger.info(f"Record {record_id} not found in {table.value} table")
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    return


@app.get("/v1/join/{table1}/{table2}/{key}")
async def join(table1: TableEnum, table2: TableEnum, key: str):
    logger.info(f"Joining {table1.value} and {table2.value} on {key}")
    records = await join_tables(
        table_map[table1.value]["table_ref"], table_map[table2.value]["table_ref"], key
    )
    if records is None:
        logger.info(f"Error joining {table1.value} and {table2.value} on {key}")
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
    return records
